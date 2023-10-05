import torch.utils.data as data

import os
import sys

def find_classes(dir):
    # The condition ensures that only directories (and not files) are added to the classes list
    classes = [d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir,d))]
    classes.sort()
    classes_to_idx = {classes[i]: i for i in range(len(classes))}
    return classes, classes_to_idx

def make_dataset(root, source):
    if not os.path.exists(source):
        print("Setting file %s for ARID doesn't exist." %(source))
        sys.exit()
    else:
        clips = []
        with open(source) as split_f:
            data = split_f.readlines()
            for line in data:
                line_info = line.split()
                clip_path = os.path.join(root, line_info[0])
                # duration = int(line_info[1])
                target = int(line_info[1])
                # item = (clip_path, duration, target)
                item = (clip_path, target)
                clips.append(item)

    return clips 

class ARID_prep(data.Dataset):
    
    def __init__(self,
                 root,
                 source,
                 phase,
                 modality,
                 name_pattern=None,
                 is_color=True,
                 num_segments=1,
                 new_length=1,
                 new_width=0,
                 new_height=0,
                 transform=None,
                 target_transform=None,
                 video_transform=None,
                 ensemble_training = False,
                 gamma= None):
        
        classes, class_to_idx = find_classes(root)
        clips = make_dataset(root, source)
        self.gamma = gamma

        if len(clips) == 0:
            raise(RuntimeError("Found 0 video clips in subfolders of: " + root + "\n"
                               "Check your data directory."))

        self.root = root
        self.source = source
        self.phase = phase
        self.modality = modality

        self.classes = classes
        self.class_to_idx = class_to_idx
        self.clips = clips
        self.ensemble_training = ensemble_training
        
        if name_pattern:
            self.name_pattern = name_pattern
        else:
            if self.modality == "rgb":
                self.name_pattern = "img_%05d.jpg"
            elif self.modality == "flow":
                self.name_pattern = "flow_%s_%05d"

        self.is_color = is_color
        self.num_segments = num_segments
        self.new_length = new_length
        self.new_width = new_width
        self.new_height = new_height

        self.transform = transform
        self.target_transform = target_transform
        self.video_transform = video_transform