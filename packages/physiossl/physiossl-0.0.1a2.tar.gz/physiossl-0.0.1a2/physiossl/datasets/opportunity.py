"""
@Time    : 2021/9/21 2:19
@File    : opportunity.py
@Software: PyCharm
@Desc    : 
"""
import os
import warnings
from typing import List

import numpy as np
import pandas as pd
import scipy.io as sio
import torch
import torch.nn as nn
from tqdm.std import tqdm
from torch.utils.data import Dataset

from .utils import minmax_scale, standard_scale


class OpportunityUCIDataset(Dataset):
    def __init__(self, data_path: str, seq_len: int, subject_list: List = None, modal: str = 'eeg',
                 return_idx: bool = False,
                 transform: nn.Module = None, verbose: bool = True, standardize: str = 'none'):
        self.data_path = data_path
        self.transform = transform
        self.subject_list = subject_list
        self.modal = modal
        self.return_idx = return_idx

        with open(os.path.join(data_path, 'column_names.txt')) as f:
            lines = f.readlines()
        column_lines = list(filter(lambda x: x.startswith('Column:'), lines))
        columns = [col.split() for col in column_lines]

        for i, patient in enumerate(tqdm(subject_list, desc='::: LOADING OPPORTUNITY DATA ::::')):
            df = pd.read_csv(os.path.join(data_path, patient), header=0, delimiter=' ')
            df.fillna(method='ffill', inplace=True)
            print(df.head(), df.shape)
