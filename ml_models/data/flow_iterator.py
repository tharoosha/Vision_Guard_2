import cv2
import os 
import numpy as np
import logging

class Flow(object):
    
    def __init__(self, vid_path):
        self.open(vid_path)

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def reset(self):
        self.close()
        self.vid_path = None
        self.frame_count = -1
        self.faulty_frame = None
        return self

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
        # offset = 0

        # if self.vid_path.endswith('.flv'):
        #     offset = -1

        # unverified_frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)) + offset
        unverified_frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # if check_validity:
        #     verified_frame_count = 0
        #     for i in range(unverified_frame_count):
        #         self.cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        #         if not self.cap.grab():
        #             logging.warning("FlowIter:: >> frame (start from 0) {} corrupted in {}".format(i, self.vid_path))
        #             break
        #         verified_frame_count = i + 1
        #     self.frame_count = verified_frame_count
        # else:
        #     self.frame_count = unverified_frame_count

        self.frame_count = unverified_frame_count
            
        assert self.frame_count > 0, "FlowIter:: Video: `{}' has no frames".format(self.vid_path)
        
        return self.frame_count
    
    def extract_frames(self, idxs, force_gray=True):
        frames = self.extract_frames_fast(idxs, force_gray)
        if frames is None:
            # try slow method:
            frames = self.extract_frames_slow(idxs, force_gray)
        return frames
    
    def extract_frames_fast(self, idxs, force_gray=True):
        assert self.cap is not None, "No opened video."

        if len(idxs) < 1:
            return []

        frames = []
        pre_idx = max(idxs)
        
        for idx in idxs:
            assert (self.frame_count < 0) or (idx < self.frame_count), \
                "idxs: {} > total valid frames({})".format(idxs, self.frame_count)
            if pre_idx != (idx - 1):
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            res, frame = self.cap.read() # in BGR/GRAY format
            pre_idx = idx
            if not res:
                self.faulty_frame = idx
                return None
            if len(frame.shape) >= 3:
                if force_gray:
                    # Convert BGR to Gray
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frames.append(frame)
        return frames
    
    def extract_frames_slow(self, idxs, force_gray=True):
        assert self.cap is not None, "No opened video."
        if len(idxs) < 1:
            return []

        frames = [None] * len(idxs)
        idx = min(idxs)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        while idx <= max(idxs):
            res, frame = self.cap.read() # in BGR/GRAY format
            if not res:
                # end of the video
                self.faulty_frame = idx
                return None
            if idx in idxs:
                # fond a frame
                if len(frame.shape) >= 3:
                    if force_gray:
                        # Convert BGR to Gray
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                pos = [k for k, i in enumerate(idxs) if i == idx]
                for k in pos:
                    frames[k] = frame
            idx += 1
        return frames
    
    def close(self):
        if hasattr(self, 'cap') and self.cap is not None:
            self.cap.release()
            self.cap = None
        return self
    
