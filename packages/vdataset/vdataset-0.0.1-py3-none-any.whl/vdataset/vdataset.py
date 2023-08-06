from torch.utils.data import Dataset
import pandas as pd
from torchvision import transforms
from PIL import Image
from pathlib import Path


class VDataset(Dataset):
    def __init__(self, csv_file: str, root_dir: str, file_format: str = "jpg", id_col_name: str = "video_id", label_col_name: str = "label", frames_limit_mode: str = None, frames_limit: int = 1, frames_limit_col_name: str = "frames", frame_resize: tuple = None, transform=None):
        """
        Load video datasets to pytorch DataLoader

        csv_file                : Path to .csv file
        root_dir                : Root Directory of the video dataset
        file_format             : File type of the frame images (.jpg, .jpeg, .png)
        id_col_name             : Column name, where id/name of the video on the .csv file
        label_col_name          : Column name, where label is on the .csv file
        frames_limit_mode       : Mode of the frame count detection ("manual", "csv" or else it auto detects all the frames available)
        frames_limit            : Number of frames in a video (required if frames_count_mode set to "manual")
        frames_limit_col_name   : Column name, where label is on the .csv file (required if frames_count_mode set to "csv")
        frames_resize           : Resize the frames (Also this can be done on using transform too)

        """
        self.dataframe = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.file_format = '*{}'.format(
            file_format) if file_format[0] == "." else '*.{}'.format(file_format)
        self.id_col_name = id_col_name
        self.label_col_name = label_col_name
        self.frames_limit_mode = frames_limit_mode
        self.frames_limit = frames_limit
        self.frames_limit_col_name = frames_limit_col_name
        self.frame_resize = frame_resize
        self.transform = transform

    def __getitem__(self, index):
        row = self.dataframe.iloc[index]
        label = row[self.label_col_name]
        video_id = row[self.id_col_name]

        if self.frames_limit_mode == "csv":
            self.frames_limit = row[self.frames_limit_col_name]

        frames_list = list(
            Path('{}/{}'.format(self.root_dir, video_id)).glob(self.file_format))

        if len(frames_list) == 0:
            raise FileNotFoundError('Error: No frames found.')
        elif (self.frames_limit_mode == "manual" or self.frames_limit_mode == "csv") and (len(frames_list) > self.frames_limit):
            frames_list = frames_list[0: self.frames_limit]

        frames = [Image.open(f).convert('RGB') for f in frames_list]

        if self.frame_resize:
            size = (self.frame_resize, self.frame_resize) if len(
                self.frame_resize) == 1 else self.frame_resize
            resize = transforms.Resize(size)
            frames = [resize(frame) for frame in frames]

        if self.transform:
            transformed_frames = [self.transform(frame) for frame in frames]
            return transformed_frames, label
        return frames, label

    def __len__(self) -> int:
        return len(self.dataframe)
