import os
import csv
import cv2

def csv_deal(csv_file:str, csv_type):
    path = "ml_models/dataset/ARID_v1.5/clips_v1.5/"

    with open(csv_file, newline="") as split_f:
        reader = csv.DictReader(split_f)
        save_txt=csv_type + '_' + "split1" + ".txt"
        
        with open(save_txt, 'w') as write_txt:
            for i,line in enumerate(reader):
                label = line["ClassID"]
                # name = line["Video"][:-4]
                name = line['Video']
                cap = cv2.VideoCapture(path+name)
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

                # duration = str(len(os.listdir(path+name)))
                # write_thing=name+' '+duration+' '+label+'\n'
                write_thing = name[:-4]+' '+str(frame_count)+' '+label+'\n'
                # print(write_thing)
                write_txt.write(write_thing)

#csv_deal("ARID1.1_t1_train_pub.csv","train")
csv_deal("ml_models/data/dataset_prep/ARID1.1_t1_test_pub.csv","ml_models/data/settings/val")
#txt_deal('train_rgb_split1.txt')