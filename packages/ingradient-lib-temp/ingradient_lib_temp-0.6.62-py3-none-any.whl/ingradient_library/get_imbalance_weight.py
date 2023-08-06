import os
import numpy as np

def get_imbalance_weight(root_dir, n_classes):
    file_list = os.listdir(root_dir)
    result = np.zeros(n_classes)
    for file in file_list:
        if 'npz' in file:
            seg = np.load(os.path.join(root_dir, file))['y']
            id, num = np.unique(seg, return_counts = True)
            result[id] += num
    
    return result.sum()/result