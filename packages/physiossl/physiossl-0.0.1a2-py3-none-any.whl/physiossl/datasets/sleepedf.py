"""
@Time    : 2021/6/23 16:46
@File    : sleepedf.py
@Software: PyCharm
@Desc    : 
"""
import os
import warnings
from typing import List

import numpy as np
import scipy.io as sio
import torch
import torch.nn as nn
from tqdm.std import tqdm
from torch.utils.data import Dataset

from .utils import minmax_scale, standard_scale


class SleepEDFDataset(Dataset):
    num_subject = 153
    fs = 100

    def __init__(self, data_path: str, seq_len: int, subject_list: List = None, modal='eeg', return_idx: bool = False,
                 transform: nn.Module = None, standardize: str = 'none'):
        assert isinstance(subject_list, list)
        assert modal in ['eeg', 'pps', 'all']

        self.data_path = data_path
        self.transform = transform
        self.subject_list = subject_list
        self.modal = modal
        self.return_idx = return_idx

        self.data = []
        self.labels = []

        for i, patient in enumerate(tqdm(subject_list, desc='::: LOADING SLEEPEDF DATA ::::')):
            data = np.load(os.path.join(data_path, patient))
            if modal == 'eeg':
                recordings = np.stack([data['eeg_fpz_cz'], data['eeg_pz_oz']], axis=1)
            elif modal == 'pps':
                recordings = np.stack([data['emg'], data['eog']], axis=1)
            elif modal == 'all':
                recordings = np.stack([data['eeg_fpz_cz'], data['eeg_pz_oz'],
                                       data['emg'], data['eog']], axis=1)
            else:
                raise ValueError

            # print(f'[INFO] Convert the unit from V to uV...')
            if standardize == 'none':
                recordings *= 1e6
            elif standardize == 'minmax':
                recordings = minmax_scale(recordings, dim=-1)
            elif standardize == 'standard':
                recordings = standard_scale(recordings, dim=-1)
            else:
                raise ValueError

            annotations = data['annotation']

            recordings = recordings[:(recordings.shape[0] // seq_len) * seq_len].reshape(-1, seq_len,
                                                                                         *recordings.shape[1:])
            annotations = annotations[:(annotations.shape[0] // seq_len) * seq_len].reshape(-1, seq_len)

            assert recordings.shape[:2] == annotations.shape[:2]

            self.data.append(recordings)
            self.labels.append(annotations)

        self.data = np.concatenate(self.data)
        self.labels = np.concatenate(self.labels)
        self.idx = np.arange(self.data.shape[0] * self.data.shape[1]).reshape(-1, self.data.shape[1])
        self.full_shape = self.data[0].shape

    def __getitem__(self, item):
        x = self.data[item]
        y = self.labels[item]

        x = x.astype(np.float32)
        y = y.astype(np.long)

        if self.transform is not None:
            x = self.transform(x)

        x = torch.from_numpy(x)
        y = torch.from_numpy(y)

        if self.return_idx:
            return x, y, torch.from_numpy(self.idx[item].astype(np.long))
        else:
            return x, y

    def __len__(self):
        return len(self.data)
