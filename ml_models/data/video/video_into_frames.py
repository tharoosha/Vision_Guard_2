import cv2
import os

# dir_names = os.listdir("datasets/vedio/clips_v1.5")[0:-1]
dir_names = os.listdir("ml_models/dataset/ARID_v1.5/clips_v1.5")
# print(dir_names)
print(os.listdir("ml_models/dataset/ARID_v1.5/clips_v1.5"))

path='ml_models/data/ARID_frames/'
for dir_name in dir_names:
    print("Processing: %s"%dir_name)
    path_dir = os.path.join(path,dir_name)
    video_names = os.listdir("ml_models/dataset/ARID_v1.5/clips_v1.5/"+dir_name)
    print(video_names)
    for name in video_names:
        cap = cv2.VideoCapture(os.path.join("ml_models/dataset/ARID_v1.5/clips_v1.5/",dir_name,name))
        if not os.path.exists(path_dir):
            os.mkdir(path_dir)
        video_path=os.path.join(path_dir,name[:-4])
        i=1
        if not os.path.exists(video_path):
            os.mkdir(video_path)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        while True:
            # Capture frame by frame
            ret, frame = cap.read()
            # ret is True if the frame is read correctly
            if not ret:
                print("Video %s processing completed"%name)
                break
            cv2.imwrite(video_path+'/img_{0:05d}.jpg'.format(i),frame)
            i+=1
        # After all operations are completed, release the capturer
        cap.release()