import scanpy as sc
import pandas as pd
import logging
from tqdm import tqdm
import torch
from sklearn.preprocessing import LabelEncoder
import torch
from torch.utils.data import Dataset
import json
import os

class SCDataset(Dataset):
    def __init__(self, tensor_dir='/', gene_set=None):

        with open(f'{tensor_dir}/metadata.json') as f:
            self.batch_metadata = json.load(f)
        with open(f'{tensor_dir}/dataset_metadata.json') as f:
            self.dataset_metadata = json.load(f)
        if 'gene_list' in self.batch_metadata:
            del self.batch_metadata['gene_list']
        self.tensor_dir = tensor_dir
        self.isddp = False
        self.bid2did = dict(zip(self.batch_metadata['batch_id'], self.batch_metadata['dataset_id']))
        self.did2gene = dict(zip(self.dataset_metadata['id'], self.dataset_metadata['gene_list']))
        if gene_set:
            gene_mask = []
            for i in self.dataset_metadata['gene_list']:
                i = set(i)
                gene_mask.append(torch.tensor([j in i for j in gene_set]).bool())
            self.did2mask = dict(zip(self.dataset_metadata['id'], gene_mask))
        else:
            self.did2mask = None

    def __len__(self):
        return len(self.batch_metadata['batch_id'])

    def __getitem__(self, idx):
        tensor_path = os.path.join(self.tensor_dir, str(self.batch_metadata['batch_id'][idx])+'.pt')
        seq = torch.load(tensor_path).coalesce()
        if self.batch_metadata['platform'][idx]=='cosmx':
            coord = torch.load(os.path.join(self.tensor_dir, str(self.batch_metadata['batch_id'][idx])+'.coord.pt'))
        else:
            coord = torch.zeros([seq.shape[0], 2]).float() - 1
        batch_id = torch.zeros(seq.shape[0]).long() + int(self.batch_metadata['batch_id'][idx])
        dataset_id = torch.zeros(seq.shape[0]).long() + int(self.batch_metadata['dataset_id'][idx])
        gene_mask = self.get_gene_mask(self.batch_metadata['dataset_id'][idx]) if self.did2mask else torch.ones(
            [seq.shape[1]]).bool()
        return seq, coord, batch_id, dataset_id, gene_mask

    def get_gene_list(self, dataset_id):
        return self.did2gene[dataset_id]

    def get_gene_mask(self, dataset_id):
        assert self.did2mask, 'gene_set was not passed when created dataset.'
        return self.did2mask[dataset_id]

    def get_partition(self, rank):
        assert self.isddp, 'Dataset is not a ddp dataset. Please call ".to_ddp()" before querying partition.'
        return self._partition(self.partitions[rank])

    def _partition(self, idx):
        assert self.isddp, 'Dataset is not a ddp dataset.'
        return SCPartitionDataset(self.batch_metadata, self.tensor_dir, idx)

    def get_valid(self):
        assert self.isddp, 'Dataset is not a ddp dataset. Please call ".to_ddp()" before querying validation set.'
        assert len(self.val_idx)>0, 'No available validation set.'
        return self._partition(self.val_idx)

    def to_ddp(self, n_partitions, max_batch_size=2000, val_num=0, val_idx=None):
        assert not self.isddp, 'Dataset is already ddp dataset.'

        if val_num>0:
            if not val_idx:
                ids = np.random.permutation(len(self.batch_metadata['batch_id']))
                self.val_idx = ids[:val_num]
                self.train_idx = ids[val_num:]
            else:
                self.train_idx = np.array([i for i in range(len(self.batch_metadata['batch_id'])) if i not in set(val_idx)])
                self.val_idx = np.array(val_idx)
            self.partitions = balanced_partition(np.array(self.batch_metadata['batch_size'])[self.train_idx], n_partitions,
                                    max_batch_size)
            new_partitions = [[] for _ in range(n_partitions)]
            for i, p in enumerate(self.partitions):
                for j in p:
                    new_partitions[i].append(self.train_idx[j])
            self.partitions = new_partitions

        else:
            self.train_idx = np.arange(len(self.batch_metadata['batch_id']))
            self.val_idx = np.array([])
            self.partitions = balanced_partition(self.batch_metadata['batch_size'], n_partitions, max_batch_size)
        self.isddp = True

class SCPartitionDataset(Dataset):
    def __init__(self, batch_metadata, tensor_dir, idx, gene_set=None):
        self.batch_metadata = {}
        for k in batch_metadata:
            self.batch_metadata[k] = [batch_metadata[k][i] for i in idx]
        self.tensor_dir = tensor_dir
        with open(f'{tensor_dir}/dataset_metadata.json') as f:
            self.dataset_metadata = json.load(f)

        self.bid2did = dict(zip(self.batch_metadata['batch_id'], self.batch_metadata['dataset_id']))
        self.did2gene = dict(zip(self.dataset_metadata['id'], self.dataset_metadata['gene_list']))

        if gene_set:
            gene_mask = []
            for i in self.dataset_metadata['gene_list']:
                i = set(i)
                gene_mask.append(torch.tensor([j in i for j in gene_set]).bool())
            self.did2mask = dict(zip(self.dataset_metadata['id'], gene_mask))
        else:
            self.did2mask = None

    def __len__(self):
        return len(self.batch_metadata['batch_id'])#//10

    def __getitem__(self, idx):
        tensor_path = os.path.join(self.tensor_dir, str(self.batch_metadata['batch_id'][idx])+'.pt')
        seq = torch.load(tensor_path).coalesce()
        if self.batch_metadata['platform'][idx]=='cosmx':
            coord = torch.load(os.path.join(self.tensor_dir, str(self.batch_metadata['batch_id'][idx])+'.coord.pt'))
        else:
            coord = torch.zeros([seq.shape[0], 2]).float() - 1
        if seq.shape[0]>2000:
            randid = torch.randperm(seq.shape[0])
            coord = coord[randid[:2000]]
            seq = seq.index_select(0, randid[:2000]).coalesce()
        batch_id = torch.zeros([seq.shape[0]]).long() + int(self.batch_metadata['batch_id'][idx])
        dataset_id = torch.zeros([seq.shape[0]]).long() + int(self.batch_metadata['dataset_id'][idx])
        gene_mask = self.get_gene_mask(self.batch_metadata['dataset_id'][idx]) if self.did2mask else torch.ones(
            [seq.shape[1]]).bool()
        seq = [seq.indices(), seq.values(), torch.tensor(seq.shape)]
        return seq, coord, batch_id, dataset_id, gene_mask

    def get_gene_list(self, dataset_id):
        return self.did2gene[dataset_id]

    def get_gene_mask(self, dataset_id):
        assert self.did2mask, 'gene_set was not passed when created dataset.'
        return self.did2mask[dataset_id]

class XDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._num = self[list(self.keys())[0]].shape[0]

    # No longer required
    # def check(self):
    #     for k, v in self.items():
    #         assert isinstance(v, torch.Tensor), f'{k} is not a torch.Tensor'
    #         assert v.shape[0] == self._num, f'{k} contains {v.shape[0]} samples. Expected: f{self._num}'

    def size(self):
        logging.info('Deprecated function: Xdict.size()')
        return self._num

    # Not usable for sparse data
    # def drop(self, ratio):
    #     drop_num = int(self._num * ratio)
    #     keep_idx = np.random.permutation(self._num)[drop_num:]
    #     for k, v in self.items():
    #         self[k] = v[keep_idx]
    #     return self

def clean_batches(data):
    # Remove batch with less than 1000 cells
    sc.pp.filter_cells(data, min_counts=5)
    remove_list = []
    for b in data.obs['batch'].value_counts().reset_index().iterrows():
        if b[1]['batch'] < 500:
            remove_list.append(b[1]['index'])
    data = data[~data.obs['batch'].isin(set(remove_list))]
    return data

import numpy as np

def balanced_partition(data, n_partitions, max_batch_size=2000):
    # Sort batches
    if torch.is_tensor(data[0]):
        batch_sizes = [(i, len(batch)) for i, batch in enumerate(data)]
    else:
        batch_sizes = [(i, batch) for i, batch in enumerate(data)]
    batch_sizes.sort(key=lambda x: x[1], reverse=True)

    # inialize partitions
    partitions = [[] for _ in range(n_partitions)]

    # Fill partitions
    j = 0
    for (i, _) in batch_sizes:
        partitions[j].append(i)
        j = (j + 1) % n_partitions
    return partitions

def stratified_sample_genes_by_sparsity(data, boundaries=None, seed=10):
    df = data.to_df()
    zero_rates = 1 - df.astype(bool).sum(axis=0) / df.shape[0]
    if boundaries is None:
        # boundaries = [0, zero_rates.mean() - zero_rates.std(), zero_rates.mean(), 
        #               min(zero_rates.mean() + zero_rates.std(), 1)]
        boundaries = [0, 0.75, 0.9, 0.95, 1]
    gene_group = pd.cut(zero_rates, boundaries, labels=False)
    # gene_df = pd.DataFrame({'zero_rates': zero_rates, 'gene_group': gene_group})
    zero_rates = zero_rates.groupby(gene_group, group_keys=False)
    samples = zero_rates.apply(lambda x: x.sample(min(len(x), 25), random_state=seed))
    return list(samples.index)

def data_setup(adata, return_sparse=True, device='cpu'):
    # Data Setup
    order = torch.arange(adata.shape[0], device=device)
    lb = LabelEncoder().fit(adata.obs['batch'])
    batch_labels = lb.transform(adata.obs['batch'])
    # print(lb.classes_)
    seq_list = [[], [], [], []] if return_sparse else []
    batch_list = []
    order_list = []
    dataset_list = []
    coord_list = []
    if adata.obs['cell_type'].dtype!=int:
        labels = LabelEncoder().fit_transform(adata.obs['cell_type'])
    else:
        labels = adata.obs['cell_type'].values
        print(labels.mean())
    label_list = []
    dataset_label = LabelEncoder().fit_transform(adata.obs['Dataset'])
    for batch in range(batch_labels.max() + 1):
        if return_sparse:
            x = (adata.X[batch_labels == batch]).astype(float)
            x = list(map(torch.from_numpy, [x.indptr, x.indices, x.data])) + [torch.tensor(x.shape)]
            for i in range(4):
                seq_list[i].append(x[i].to(device))
        else:
            x = torch.from_numpy(adata.X[batch_labels == batch].todense()).float()
            seq_list.append(x.to(device))
        # x = torch.sparse_csr_tensor(x.indptr, x.indices, x.data, (x.shape[0], x.shape[1])).to_sparse().float()
        # seq_list.append(x)
        order_list.append(order[batch_labels == batch])
        dataset_list.append(torch.from_numpy(dataset_label[batch_labels == batch]).long().to(device))
        batch_list.append(torch.from_numpy(batch_labels[batch_labels == batch]).to(device))
        if adata.obs['platform'][batch_labels == batch][0] == 'cosmx':
            coord_list.append(torch.from_numpy(adata.obs[['x_FOV_px', 'y_FOV_px']][batch_labels == batch].values).to(device))
        else:
            coord_list.append(torch.zeros(order_list[-1].shape[0], 2).to(device) - 1)
        label_list.append(torch.from_numpy(labels[batch_labels == batch].astype(int)).to(device))
    del order
    return seq_list, batch_list, batch_labels, order_list, dataset_list, coord_list, label_list