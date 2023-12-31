import os
import csv

def csv_deal(csv_file:str):
    path = 'ARID_predict_farmes/'
    field_names = ['VideoID', "duration"]
    pred_rows = []
    with open(csv_file, newline="") as split_f:
        reader = csv.DictReader(split_f)   #Use the first row as the key value
        save_csv = "predict.csv"
        for i, line in enumerate(reader):
            VideoID = line["VideoID"]  #Video name
            duration = str(len(os.listdir(path + VideoID)))
            pred_row = {field_names[0]: VideoID, field_names[1]: duration}
            pred_rows.append(pred_row)
            print("Writing: Video: "+VideoID+'Frame number:'+duration)

    with open(save_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        for pred_row in pred_rows:
            writer.writerow(pred_row)

csv_deal("ARID1.1_t1_validation_gt_pub.csv")
# txt_deal('train_rgb_split1.txt')