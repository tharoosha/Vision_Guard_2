import cv2
import os 
import numpy as np
import logging

class Flow(object):
    
    def __init__(self, vid_path):
        self.open(vid_path)

    def open(self, vid_path):
        assert os.path.exists(vid_path), "FlowIter:: cannot locate: `{}'".format(vid_path)

        # close previous video & reset variables
        # self.reset()

        # try to open video
        cap = cv2.VideoCapture(vid_path)
        if cap.isOpened():
            self.cap = cap
            self.vid_path = vid_path
        else:
            raise IOError("FlowIter:: failed to open video: `{}'".format(vid_path))

        return self
    
    def count_frames(self, check_validity=False):
        offset = 0

        # if self.vid_path.endswith('.flv'):
        #     offset = -1

        unverified_frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)) + offset

        if check_validity:
            verified_frame_count = 0
            for i in range(unverified_frame_count):
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                if not self.cap.grab():
                    logging.warning("FlowIter:: >> frame (start from 0) {} corrupted in {}".format(i, self.vid_path))
                    break
                verified_frame_count = i + 1
            self.frame_count = verified_frame_count
        else:
            self.frame_count = unverified_frame_count
        assert self.frame_count > 0, "FlowIter:: Video: `{}' has no frames".format(self.vid_path)
        
        return self.frame_count