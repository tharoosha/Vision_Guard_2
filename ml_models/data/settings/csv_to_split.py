import os
import csv

def csv_deal(csv_file:str, csv_type):
    path = "ARID/"

    with open(csv_file, newline="") as split_f:
        reader = csv.DictReader(split_f)
        save_txt=csv_type + '_' + "split1" + ".txt"
        
        with open(save_txt, 'w') as write_txt:
            for i,line in enumerate(reader):
                label = line["ClassID"]
                name = line["Video"][:-4]
                # duration = str(len(os.listdir(path+name)))
                # write_thing=name+' '+duration+' '+label+'\n'
                write_thing = name+' '+label+'\n'
                # print(write_thing)
                write_txt.write(write_thing)

#csv_deal("ARID1.1_t1_train_pub.csv","train")
csv_deal("ml_models/dataset/dataset_prep/ARID1.1_t1_train_pub.csv","train")
#txt_deal('train_rgb_split1.txt')