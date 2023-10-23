import os
import csv

def csv_deal(csv_file:str,csv_type):
    path='ml_models/data/ARID_frames/'
    with open(csv_file, 'r') as split_f:

        # reader = csv.DictReader(split_f)   #Use the first row as the key value
        reader = split_f.readlines()
        save_txt=csv_type + '_' + "split1" + ".txt"

        with open(save_txt, 'w') as write_txt:
            for line in reader:
                parts = line.strip().split('\t')
                print(parts[-1][:-4])
                
                VideoID = parts[0]
                ClassID = parts[1]
                Video = parts[-1][:-4]

                # print(VideoID,Video,ClassID)
                # Extract the video file name
                # video_path = parts[2]
                # video_name = video_path.split('/')[-1]
                # simplified_name = video_name.split('_')[-1]
            # for i,line in enumerate(reader):
                # print(line.split(" "))
                # label = line["ClassID"]  # Video type
                # name = line["Video"][:-4]  # Video name
                # print(path+name)

                print(path+Video)
                duration = str(len(os.listdir(path+Video)))
                # write_thing=VideoID+' '+duration+' '+ClassID+'\n'
                
                # write_thing=name+' '+label+'\n'
                # print("Writing: Video: "+name+' Label:'+label)
                # print("Writing: Video: "+name+' Frame number:'+duration+' Label:'+label)
                # write_txt.write(write_thing)
                # print(write_thing)

# csv_deal("datasets/settings/ARID/ARID1.1_t1_train_pub.csv","datasets/settings/ARID/train")
csv_deal("ml_models/dataset/ARID_v1.5/list_cvt/split_0/ref/ARID1.1_t1_test.txt","ml_models/data/settings/ARID/val")
#txt_deal('train_rgb_split1.txt')