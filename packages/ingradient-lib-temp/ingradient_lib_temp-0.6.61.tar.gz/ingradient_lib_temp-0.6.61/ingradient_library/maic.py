from torch.utils.data import Dataset
from ingradient_library.transform import Transform
from ingradient_library.preprocessing import *
from ingradient_library.get_nnunet_setting import get_transform_params
import torch
import numpy as np
import os
import h5py
import copy

class MAIC_Sampling(object):
    def __init__(self, transform = Transform(*get_transform_params(None))):
        self.transform = transform
    def __call__(self, images, seg = None, train = True, is_CT = True):
        temp = copy.deepcopy(images)
        if is_CT:
            temp[np.where(temp < - 700)] = 0
        non_zero_index = np.where(temp.astype(int) != 0)
        min_val = np.min(non_zero_index, axis = 1)
        max_val = np.max(non_zero_index, axis = 1)
        random_move = np.random.randint([-5,-5,-15], [5, 5, 15])
        images = images[:, min_val[-3]:max_val[-3]+1, min_val[-2]:max_val[-2]+1, min_val[-1]:max_val[-1]+1]
        z_start = int(images.shape[-1] * 0.25)
        z_term = 96
        y_start = images.shape[-2]//2 - 32
        y_end= images.shape[-2]//2 + 32
        x_term = 64
        images = images[:, 5 + random_move[0]:x_term+random_move[0]+5, y_start+random_move[1]:y_end+random_move[1],
                       -(z_start + z_term) + random_move[2]:-z_start + random_move[2]]
        if train:
            seg = seg[min_val[-3]:max_val[-3]+1, min_val[-2]:max_val[-2]+1, min_val[-1]:max_val[-1]+1]
            seg = seg[5 + random_move[0]:x_term+random_move[0]+5, y_start+random_move[1]:y_end+random_move[1],
                       -(z_start + z_term) + random_move[2]:-z_start + random_move[2]]
            images = torch.tensor(images).unsqueeze(0).double()
            seg = torch.tensor(seg).unsqueeze(0).long()
            if self.transform != None:
                images, seg = self.transform(images, seg, None)
            images = images.squeeze(0).numpy()
            seg = seg.squeeze(0).numpy()
        else: 
            seg = None

        return images, seg


class MAIC_Dataset(Dataset):
    def __init__(self, path = None, normalizer = Normalizer([0.05, 0.95]), train = True, transform = Transform(*get_transform_params(None))):
        if path == None:
            path = '../mnt/dataset/'
        
        self.path = path
        self.file_list = []
        for f in os.listdir(path):
            if not 'py' in f:
                self.file_list.append(f)
        
        self.file_list = sorted(self.file_list)

        self.normalizer = normalizer
        self.train = train
        self.sampler = MAIC_Sampling(transform = transform)
        
    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        current_file = os.path.join(self.path, self.file_list[idx])
        hdf_file = h5py.File(current_file , 'r')
        CT = np.array(hdf_file['CT'])
        PET = np.array(hdf_file['PET'])
        spacing = np.array(hdf_file['Size'])
        images = np.stack((CT, PET))
        
        if self.train:
            seg = np.array(hdf_file['Aorta'])

        hdf_file.close()
        
        images, seg = self.sampler(images, seg, train = self.train)
        if self.normalizer:
            images = self.normalizer(images)
            images = images.numpy()
        
        return images, seg, spacing, CT.shape