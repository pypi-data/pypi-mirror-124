from ingradient_library.preprocessing import Cropping
import SimpleITK as sitk
import pickle
import os
import numpy as np

class Data_Organizer(object):
    def __init__(self, PATH, SAVE_PATH, ID):
        self.crop = Cropping
        self.PATH = PATH
        self.SAVE_PATH = SAVE_PATH
        self.ID = ID
    

    def run(self, seg_path, img_path, index):
        seg = sitk.ReadImage(seg_path)
        img = sitk.ReadImage(img_path)
        save_dict = dict()
        save_dict['spacing'] = img.GetSpacing()
        save_dict['direction'] = img.GetDirection()
        save_dict['origin'] = img.GetOrigin()
        img = sitk.GetArrayFromImage(img)
        seg = sitk.GetArrayFromImage(seg)
        save_path = os.path.join(self.SAVE_PATH, 'COVID_'+str(index)+'_info.pkl')
        pickle_file = open(save_path, 'wb')
        pickle.dump(save_dict, pickle_file)
        pickle_file.close()
        img_arr, seg_arr = self.crop(np.expand_dims(img, axis = 0), seg)
        np.savez(os.path.join(self.SAVE_PATH, 'COVID_'+str(index)+'.npz'), x =img_arr, y=seg_arr)