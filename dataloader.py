
import os
from matplotlib.patches import FancyArrowPatch
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
import glob


# setting
data_seg = 25    # 데이터를 몇개씩 가져올지
batch_size = 64  # 배치-사이즈


class CustomDataset(Dataset):
    def __init__(self, data_path, data_seg):
        self.data = []

        for file in data_path:
            # print(file)
            try:
                df = pd.read_csv(file)
                for i in range(0, len(df.index), data_seg):
                    if i+data_seg > len(df.index):
                        break
                    temp_x = df.values[i:i+data_seg]
                    if file[-6] == '_':
                        temp_y = file[-5:-4]
                    else:
                        temp_y = file[-6:-4]
                    self.data.append((temp_x, int(temp_y)-1))
                    # print((temp_x, int(temp_y)))
            except ValueError:
                continue

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        x, y = self.data[idx]
        x = np.expand_dims(x, axis=0)
        x = torch.FloatTensor(x)
        # y = torch.IntTensor(y)
        return x, y

current_path = os.getcwd()
train_path = glob.glob(current_path + '/output/**', recursive=True)
data_path = []
for i in train_path:
    if os.path.isfile(i):
        data_path.append(i)



train = CustomDataset(data_path, data_seg)

## data split
from sklearn.model_selection import train_test_split
from torch.utils.data import Subset
datasets={}
train_idx, temp_idx = train_test_split(list(range(len(train))), test_size=0.2, random_state=555)
datasets['train'] = Subset(train, train_idx)
temp_dataset = Subset(train, temp_idx)
valid_idx, test_idx = train_test_split(list(range(len(temp_dataset))), test_size=0.5, random_state=555)
datasets['valid'] = Subset(temp_dataset, valid_idx)
datasets['test'] = Subset(temp_dataset, test_idx)

print("Number of Training set : ", len(datasets['train']))
print("Number of  Validation set : ", len(datasets['valid']))
print("Number of Test set : ", len(datasets['test']))



## data loader 선언
dataloaders = {}
dataloaders['train'] = DataLoader(datasets['train'], batch_size=batch_size, shuffle=True, drop_last=True)
dataloaders['valid'] = DataLoader(datasets['valid'], batch_size=batch_size, shuffle=False, drop_last=True)
dataloaders['test']  = DataLoader(datasets['test'], batch_size=batch_size, shuffle=False, drop_last=True)

