#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='cellplm',
    version='0.1.0',
    author='Hongzhi Wen',
    author_email='wenhongz@msu.edu',
    url='https://github.com/OmicsML/CellPLM',
    description=u'Package of CellPLM: A pretrain-ed cell language model beyond single cells.',
    packages=['CellPLM'],
    install_requires=[
        'torch==1.13.0+cu117',
        'einops',
        'torchmetrics',
        'wandb',
        'hdf5plugin',
        'mygene',
    ],
    dependency_links=[
        'https://download.pytorch.org/whl/cu117'
    ],
    entry_points={
    }
)