## Tutorial Notebooks

We plan to gradually release tutorials for different downstream tasks, including:

- [x] Cell-type Annotation
- [x] Spatial Imputation
- [x] Zero-shot Cell Embedding
- [ ] Gene Perturbation Prediction

~We also plan to build a more user-friendly interface for downstream tasks, therefore, the tutorials might be updated from time to time.~
The cell-type annotation tutorial is updated on 12/05/2023.  A unified `pipeline` module is now added for downstream analyses.

## Dataset Preparation

Before running the tutorial, please download datasets from our [dropbox](https://www.dropbox.com/scl/fo/i5rmxgtqzg7iykt2e9uqm/h?rlkey=o8hi0xads9ol07o48jdityzv1&dl=0) and placed h5ad datasets in the `../data` folder.

All datasets used in our tutorials are collected from previous publications and we provide the references in `../data/README.md`.

## Customized Dataset

The customized dataset can now be easily processed with `CellPLM.pipeline` module. Please refer to the tutorial of each downstream task.
