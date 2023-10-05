from data import flow_iterator
from data.dataset_prep.ARID_prep import ARID_prep


class Model(object):
    def __init__(self, vid_path):
        self.flow = flow_iterator.Flow(vid_path)

    def process(self):
        # process the flow frames here
        # for frame in self.flow:
        #     # do something with the frame
        #     pass
        frame_count = self.flow.count_frames()
        return frame_count

if __name__ == '__main__':
    vid_path = 'ml_models/dataset/ARID_v1.5/clips_v1.5_avi/Drink/Drink_1_1.avi'

    # model = Model(vid_path)
    # frame_count = model.process()
    # print(frame_count)
    dataset = ARID_prep(root='ml_models/dataset/ARID_v1.5/clips_v1.5_avi', source='ml_models/data/settings/train_split1.txt', phase='train', modality='RGB')
    print(dataset.classes)
    print(dataset.clips)
    print(dataset.class_to_idx)

