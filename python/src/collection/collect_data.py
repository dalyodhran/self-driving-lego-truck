import os

from pandas import DataFrame
from python.src.collection.data_collection import DataCollection
from python.src.motor.motor_impl import current_pos
from camera_module import takeImg


class CollectData:
    data_collection_folder = ''
    folder_count = 0
    data_collection_list = []
    next_folder = ''

    def __init__(self):
        self.data_collection_folder = os.path.join(os.getcwd(), '../../../DataCollected')
        self.folder_count = len(os.listdir(self.data_collection_folder)) // 2
        self.next_folder = os.path.join(self.data_collection_folder, "IMG"+str(self.folder_count))

    def collect_frame_data(self):
        steering = current_pos()
        frame_Path = takeImg(self.next_folder)
        data = DataCollection(frame_Path, steering)
        self.data_collection_list.append(data)

    def save_frame_data(self):
        image_list = [image for image, _ in self.data_collection_list]
        rawData = {'Image': image_list,
                   'Steering': [steering for _, steering in self.data_collection_list]}
        df = DataFrame(rawData)
        df.to_csv(os.path.join(
            self.data_collection_folder,
            f'log_{str(self.folder_count)}.csv'),
            index=False,
            header=False)
        print('Log Saved')
        print(f'Total Images: {len(image_list)}')
