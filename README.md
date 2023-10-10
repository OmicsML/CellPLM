# CellPLM
This is the official codebase for [CellPLM: Pre-training of Cell Language Model Beyond Single Cells](https://www.biorxiv.org/content/10.1101/2023.10.03.560734).

[![Preprint](https://img.shields.io/badge/Preprint-bioRxiv-brightgreen)](https://www.biorxiv.org/content/10.1101/2023.10.03.560734)
[![License](https://img.shields.io/badge/License-BSD_2--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause)

***CellPLM*** is the first single-***Cell*** ***P***re-trained ***L***anguage ***M***odel that encodes cell-cell relations and it consistently outperforms existing pre-trained and non-pre-trained models in diverse downstream tasks, with 100x higher inference speed compared to existing pre-trained models.

## Installation
We plan to release our project on PyPI soon. For now, please follow the instruction below to set up the environment for CellPLM:
### Quick Installaton
```
git clone git@github.com:OmicsML/cellplm.git && cd cellplm
pip install -r requirements.txt
```

### Complete Installation (recommended for HPC users)
```
conda create -n cellplm python=3.9 -y && conda activate cellplm
conda install cudatoolkit=11.7 -c pytorch -c nvidia
pip install torch==1.13.0+cu117 --extra-index-url https://download.pytorch.org/whl/cu117
pip install einops ipdb pydance torchmetrics wandb hdf5plugin dgl mygene
```
We recommend using `python 3.9` and `cuda 11.7` but they are adjustable.

## Tutorials
We offer several [notebooks](https://github.com/OmicsML/CellPLM/tree/main/tutorials) for various downstream tasks as introductory tutorials. 

We are also working on developing more streamlined protocols for supported tasks and a comprehensive documentation. We aim to release these by the end of the year.

## Pretrained CellPLM Model Checkpoints
The checkpoint can be acquired from our [dropbox](https://www.dropbox.com/scl/fo/i5rmxgtqzg7iykt2e9uqm/h?rlkey=o8hi0xads9ol07o48jdityzv1&dl=0). We might update our checkpoints from time to time.

[10/10/2023] The latest version is `20230926_85M`.

## Citation
```
@article{wen2023cellplm,
  title={CellPLM: Pre-training of Cell Language Model Beyond Single Cells},
  author={Wen, Hongzhi and Tang, Wenzhuo and Dai, Xinnan and Ding, Jiayuan and Jin, Wei and Xie, Yuying and Tang, Jiliang},
  journal={bioRxiv},
  pages={2023--10},
  year={2023},
  publisher={Cold Spring Harbor Laboratory}
}
```
