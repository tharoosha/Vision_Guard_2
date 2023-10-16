# from data import flow_iterator
# from data.dataset_prep.ARID_prep import ARID_prep
# import argparse
# import csv
# import os

# from tensorboardX import SummaryWriter


# parser = argparse.ArgumentParser(description='PyTorch Two-Stream Action Recognition')



# # class Model(object):
# #     def __init__(self, vid_path):
# #         self.flow = flow_iterator.Flow(vid_path)

# #     def process(self):
# #         # process the flow frames here
# #         # for frame in self.flow:
# #         #     # do something with the frame
# #         #     pass
# #         frame_count = self.flow.count_frames()
# #         return frame_count
    
# def main():
#     global args, best_prec1, model, writer, best_loss, length, width, height, input_size, scheduler, suffix
#     args = parser.parse_args()

#     training_continue = args.contine
#     if not args.no_attention:
#         args.arch='dark_light_noAttention'

#     suffix = 'ga=%s_b=%s_both_flow=%s' % (args.gamma , args.batch_size , args.both_flow)
#     headers = ['epoch', 'top1', 'top5', 'loss']
#     with open('train_record_%s.csv' % suffix, 'w', newline='') as f:
#         record = csv.writer(f)
#         record.writerow(headers)

#     with open('validate_record_%s.csv' % suffix, 'w', newline='') as f:
#         record = csv.writer(f)
#         record.writerow(headers)

#     print('work in both_flow = %s, gamma = %s, batch_size = %s'%(args.both_flow, args.gamma, args.batch_size))
    
#     input_size = 112
#     width = 170
#     height = 128

#     saveLocation="./checkpoint/"+args.dataset+"_"+args.arch+"_split"+str(args.split)
#     if not os.path.exists(saveLocation):
#         os.makedirs(saveLocation)
#     writer = SummaryWriter(saveLocation)

#     # create model

#     if args.evaluate:
#         print("Building validation model ... ")
#         model = build_model_validate()
#         optimizer = AdamW(model.parameters(), lr= args.lr, weight_decay=args.weight_decay)
#     elif training_continue:
#         model, startEpoch, optimizer, best_prec1 = build_model_continue()
#         for param_group in optimizer.param_groups:
#             lr = param_group['lr']
#         print("Continuing with best precision: %.3f and start epoch %d and lr: %f" %(best_prec1,startEpoch,lr))
#     else:
#         print("Building model with ADAMW... ")
#         model = build_model()
#         optimizer = AdamW(model.parameters(), lr= args.lr, weight_decay=args.weight_decay)
#         startEpoch = 0

# if __name__ == '__main__':
#     vid_path = 'ml_models/dataset/ARID_v1.5/clips_v1.5_avi/Drink/Drink_1_1.avi'

#     # model = Model(vid_path)
#     # frame_count = model.process()
#     # print(frame_count)
#     dataset = ARID_prep(root='ml_models/dataset/ARID_v1.5/clips_v1.5_avi', source='ml_models/data/settings/train_split1.txt', phase='train', modality='RGB')
#     print(dataset.classes)
#     print(dataset.clips)
#     print(dataset.class_to_idx)

