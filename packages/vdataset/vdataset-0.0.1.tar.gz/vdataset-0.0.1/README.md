# VDataset

## Description

Load video datasets to PyTorch DataLoader. (Custom Video Data set for PyTorch DataLoader)

## Required Libraries

* torch
* torchvision
* Pillow
* pandas

## Arguments for constructor

| Argument | Type | Required | Description|
|----------|------|----------|------------|
| csv_file  | str  | True     | Path to .csv file|
| root_dir | str  | True     | Root Directory of the video dataset|
| file_format| str | False    | File type of the frame images (ex: .jpg, .jpeg, .png)|
| id_col_name | str | False   | Column name, where id/name of the video on the .csv file|
| label_col_name | str | False | Column name, where label is on the .csv file |
| frames_limit_mode | str/None | False | Mode of the frame count detection ("manual", "csv" or else it auto detects all the frames available) |
| frames_limit | int | False | Number of frames in a video (required if frames_count_mode set to "manual") |
| frames_limit_col_name | str | False |Column name, where label is on the .csv file (required if frames_count_mode set to "csv") |
| frames_resize | tuple/None | False |        Resize the frames (Also this can be done on using transform too) |

## Usage

```python
from torch.utils.data import DataLoader
from torchvision import transforms

transforms = transforms.Compose([transforms.Resize((100, 100)),
                                       transforms.ToTensor()])

vdataset = VDataset(csv_file='path-to-csv-file.csv', root_dir='path-to-video-dir', transform=transforms)
dataloader = DataLoader(vdataset, batch_size=64) # use in DataLoader


for image, label in dataloader: # Do what do you want in dataset
    print(image, label)
    break

```
