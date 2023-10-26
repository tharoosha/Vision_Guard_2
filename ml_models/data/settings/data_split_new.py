import os
import random
import cv2

#change the directry 
dir_names = os.listdir("/content/drive/MyDrive/ARID/ARID_Extracted/clips_v1.5")

# List of main folders with their corresponding class encoding
main_folders = {}  # Add your main folders and encodings here
temp=1
for i in dir_names:

    main_folders[i]=temp
    temp+=1
print(main_folders)


# Set the ratios for train, validation, and test sets
train_ratio = 0.6
val_ratio = 0.25
test_ratio = 0.15

# Initialize lists to store subfolder names, frame counts, and encoded class indices for each set
train_info = []
val_info = []
test_info = []

def count_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return frame_count

for main_folder, class_encoding in main_folders.items():
    main_folder_path = os.path.join("/content/drive/MyDrive/ARID/ARID_Extracted/clips_v1.5/", main_folder)  # Replace "your_base_directory" with the base directory path
    video_files = [video for video in os.listdir(main_folder_path) if video.endswith('.mp4')]
    
    # Calculate the number of videos for each set
    num_videos = len(video_files)
    num_train = int(train_ratio * num_videos)
    num_val = int(val_ratio * num_videos)
    
    # Shuffle the videos randomly
    random.shuffle(video_files)
    
    for i, video in enumerate(video_files):
        
        video_path = os.path.join(main_folder_path, video)
        frame_count = count_frames(video_path)
        info = f"{main_folder}/{video[:-4]} {frame_count} {class_encoding}"
        
        if i < num_train:
            train_info.append(info)
        elif i < num_train + num_val:
            val_info.append(info)
        else:
            test_info.append(info)

# Define file paths for saving the video information
train_txt = "train.txt"
val_txt = "val.txt"
test_txt = "test.txt"

# Save the video information into the respective text files
with open(train_txt, "w") as train_file:
    train_file.write("\n".join(train_info))

with open(val_txt, "w") as val_file:
    val_file.write("\n".join(val_info))

with open(test_txt, "w") as test_file:
    test_file.write("\n".join(test_info))
