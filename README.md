# CellPLM
This is the official codebase for [CellPLM: Pre-training of Cell Language Model Beyond Single Cells](https://openreview.net/forum?id=BKXvPDekud). **The paper has been accepted by ICLR 2024 conference.** 

![Paper](https://img.shields.io/badge/Paper-ICLR24-brightgreen?link=https%3A%2F%2Fopenreview.net%2Fforum%3Fid%3DBKXvPDekud)
[![License](https://img.shields.io/badge/License-BSD_2--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause)

***CellPLM*** is the first single-***Cell*** ***P***re-trained ***L***anguage ***M***odel that encodes cell-cell relations and it consistently outperforms existing pre-trained and non-pre-trained models in diverse downstream tasks, with 100x higher inference speed compared to existing pre-trained models. You can also find a brilliant blog about the idea of CellPLM [here](https://portal.valencelabs.com/blogs/post/cellplm-pre-training-of-cell-language-model-beyond-single-cells-wKScCQHIyicpXbx).

## Installation
We recommend PyPI for quick installation. We recommend using `python 3.9` and `cuda>=11.7` but they are adjustable.

### Quick Installation with PyPI
Make sure gpu version of pytorch (>=1.13.0) has been installed before installing CellPLM.
```
pip install cellplm
```

### Full Installation (recommended for HPC users and developers)
```
conda create -n cellplm python=3.9 -y && conda activate cellplm
conda install cudatoolkit=11.7 -c pytorch -c nvidia
pip install -r requirements.txt
```
The full installation will install the same environment as we used during development. This includes `rapids` used to accelerate evaluation.

## Tutorials
We offer several [notebooks](https://github.com/OmicsML/CellPLM/tree/main/tutorials) for various downstream tasks as introductory tutorials. _Our latest studies demonstrate CellPLM is competitive on cell-type annotation tasks compared to other SOTA methods and pretrained models. The result table is shown below:_

| Method | PBMC12K | Pancreas | HLCA | Immune | Brain | Liver |
| --- | --- | --- | --- | --- | --- | --- |
| SingleCellNet | 0.845+-0.0064 | 0.644+-0.0006 | 0.811+-0.0046 | 0.775+-0.0009 | 0.877+-0.0033 | 0.872+-0.0023 |
| ACTINN | 0.614+-0.0709 | 0.528+-0.0926 | 0.218+-0.0440 | 0.236+-0.0300 | 0.695+-0.0624 | 0.614+-0.0349 |
| scANVI | 0.930+-0.0148 | 0.963+-0.0083 | 0.708+-0.0183 | 0.851+-0.0133 | 0.933+-0.0010 | **0.908+-0.0144** |
| CellTypist | 0.883+-0.0055 | 0.882+-0.0011 | 0.776+-0.0079 | 0.822+-0.0020 | 0.901+-0.0031 | 0.764+-0.0132 |
| scDiff | 0.967+-0.0042 | **0.968+-0.0143** | **0.893+-0.0070** | 0.844+-0.0076 | 0.947+-0.0074 | 0.844+-0.0042 |
| scGPT | 0.963 | 0.954 | 0.863 | ***0.907*** | **0.950** | 0.864 |
| Geneformer | ***0.979*** | - | 0.833 | 0.856 | 0.934 | 0.871 |
| CellPLM | **0.975** | ***0.983*** | ***0.929*** | **0.902** | ***0.967*** | ***0.913*** |

_(The evaluation follows the setting in [scDiff](https://www.biorxiv.org/content/10.1101/2023.10.13.562243v1.abstract) paper)_

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
