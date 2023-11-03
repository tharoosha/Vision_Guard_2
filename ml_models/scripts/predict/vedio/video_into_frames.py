import cv2
import os
path='../ARID_predict_farmes/'
path_dir = path
vedio_names = os.listdir()[0:-1]
for name in vedio_names:
    cap = cv2.VideoCapture(name)
    if not os.path.exists(path_dir):
        os.mkdir(path_dir)
    vedio_path=os.path.join(path_dir,name[:-4])
    i=1
    if not os.path.exists(vedio_path):
        os.mkdir(vedio_path)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame by frame
        ret, frame = cap.read()
        # If the frame is read correctly, ret is True
        if not ret:
            print("视频 %s 处理完成"%name)
            break
        cv2.imwrite(vedio_path+'\img_{0:05d}.jpg'.format(i),frame)
        i+=1
    # After all operations are completed, release the capturer    
    cap.release()