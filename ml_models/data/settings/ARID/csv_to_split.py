import os
import csv
def csv_deal(csv_file:str,csv_type):
    path='ml_models/data/ARID_frames/'
    with open(csv_file, newline="") as split_f:
        reader = csv.DictReader(split_f)   #Use the first row as the key value
        save_txt=csv_type + '_' + "split1" + ".txt"
        with open(save_txt, 'w') as write_txt:
            for i,line in enumerate(reader):
                label = line["ClassID"]  # Video type
                name = line["Video"][:-4]  # Video name
                # print(path+name)
                duration = str(len(os.listdir(path+name)))
                write_thing=name+' '+duration+' '+label+'\n'
                # write_thing=name+' '+label+'\n'
                # print("Writing: Video: "+name+' Label:'+label)
                # print("Writing: Video: "+name+' Frame number:'+duration+' Label:'+label)
                write_txt.write(write_thing)

csv_deal("ml_models/data/settings/ARID/ARID1.1_t1_train_pub.csv","ml_models/data/settings/ARID/train")
# csv_deal("datasets/settings/ARID/ARID1.1_t1_test_pub.csv","datasets/settings/ARID/val")
#txt_deal('train_rgb_split1.txt')