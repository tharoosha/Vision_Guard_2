import os 
import time
import argparse
import shutil
import numpy as np

import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.mps as mps

import torch.optim 
import torch.utils.data

from tensorboardX import SummaryWriter

from torch.optim import lr_scheduler
import vidoe_transforms.video_transforms
import models
import data

#import swats
from opt.AdamW import AdamW

import csv

device = 'mps' if torch.backends.mps.is_available() else "cpu"


model_names = sorted(name for name in models.__dict__
    if not name.startswith("__")
    and callable(models.__dict__[name]))

dataset_names = sorted(name for name in datasets.__all__)

parser = argparse.ArgumentParser(description='PyTorch Two-Stream Action Recognition')

best_prec1 = 0
best_loss = 30
warmUpEpoch = 5

def main():
    global args, best_prec1, model, writer, best_loss, length, width, height, input_size, scheduler, suffix
    args = parser.parse_args()
    training_continue = args.contine

    if not args.no_attention:
        args.arch = 'dark_light_noAttention'

    suffix = "ga=%s_b=%s_both_flow=%s" % (args.gamma, args.batch_size, args.both_flow)
    headers = ['epoch', 'top1', 'top5', 'loss']
    with open ('train_record_%s.csv' % suffix, 'w', newline='') as f:
        record = csv.writer(f)
        record.writerow(headers)

    with open ('validate_record_%s.csv' % suffix, 'w', newline='') as f:
        record = csv.writer(f)
        record.writerow(headers)

    print('work in both_flow = %s, gamma = %s, batch_size = %s'%(args.both_flow, args.gamma, args.batch_size))

    input_size = 112
    width = 170
    height = 128

    saveLocation="./checkpoint/"+args.dataset+"_"+args.arch+"_split"+str(args.split)
    if not os.path.exists(saveLocation):
        os.makedirs(saveLocation)
    writer = SummaryWriter(saveLocation)


    # create model

    if args.evaluate:
        print("Building validation model ... ")
        model = build_model_validate()
        optimizer = AdamW(model.parameter(), lr = args.lr, weight_decay = args.weight_decay)
    elif training_continue:
        model, startEpoch, optimizer, best_prec1 = build_model_continue()
        for param_group in optimizer.param_groups:
            lr = param_group['lr']
        print("Continuing with best precision: %.3f and start epoch %d and lr: %f" %(best_prec1,startEpoch,lr))
    else:
        print("Building model with ADAMW... ")
        model = build_model()
        optimizer = AdamW(model.parameters(), lr= args.lr, weight_decay=args.weight_decay)
        startEpoch = 0

    print("MOdel %s is loaded. " % (args.arch))

    # define loss function (criterion) and optimizer
    criterion = nn.CrossEntropyLoss().to(device)

    scheduler = lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=5, verbose=True)

    print("Saving everything to directory %s." % (saveLocation))
    dataset = "data/ARID_frames"

    mps.benchmark = True
    length = 64

    #Data transforming
    is_color = True
    scale_ratios = [1.0, 0.875, 0.75, 0.66]
    clip_mean = [0.485, 0.456, 0.406] * args.num_seg * length
    clip_std = [0.229, 0.224, 0.225] * args.num_seg * length

    train_transform = video_transforms.Compose([
            video_transforms.MultiScaleCrop((input_size, input_size), scale_ratios),
            video_transforms.RandomHorizontalFlip(),
            video_transforms.ToTensor(),
            normalize,
        ])

    val_transform = video_transforms.Compose([
            video_transforms.CenterCrop((input_size)),
            video_transforms.ToTensor(),
            normalize,
        ])
    
    # data loading 
    train_setting_file = "train_split%d.txt" % (args.split)
    train_split_file = os.path.join(args.settings, args.dataset, train_setting_file)
    val_setting_file = "val_split%d.txt" % (args.split)
    val_split_file = os.path.join(args.settings, args.dataset, val_setting_file)
    if not os.path.exists(train_split_file) or not os.path.exists(val_split_file):
        print("No split file exists in %s directory. Preprocess the dataset first" % (args.settings))
    
    # ARID.py
    train_dataset = data.__dict__[args.dataset](root=dataset,
                                                    modality="rgb",
                                                    source=train_split_file,
                                                    phase="train",
                                                    is_color=is_color,
                                                    new_length=length,
                                                    new_width=width,
                                                    new_height=height,
                                                    video_transform=train_transform,
                                                    num_segments=args.num_seg,
                                                    gamma=args.gamma)
    
    val_dataset = data.__dict__[args.dataset](root=dataset,
                                                  modality="rgb",
                                                  source=val_split_file,
                                                  phase="val",
                                                  is_color=is_color,
                                                  new_length=length,
                                                  new_width=width,
                                                  new_height=height,
                                                  video_transform=val_transform,
                                                  num_segments=args.num_seg,
                                                  gamma=args.gamma)

    print('{} samples found, {} train data and {} test data.'.format(len(val_dataset)+len(train_dataset),
                                                                           len(train_dataset),
                                                                           len(val_dataset)))

    train_loader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=args.batch_size, shuffle=True,
        num_workers=args.workers, pin_memory=True)
    print(train_loader)
    val_loader = torch.utils.data.DataLoader(
        val_dataset,
        batch_size=args.batch_size, shuffle=False,
        num_workers=args.workers, pin_memory=True)

    if args.evaluate:
        prec1,prec5,lossClassification = validate(val_loader, model, criterion, -1)
        return

    for epoch in range(startEpoch, args.epochs):
#        if learning_rate_index > max_learning_rate_decay_count:
#            break
#        adjust_learning_rate(optimizer, epoch)
        train(train_loader, model, criterion, optimizer, epoch)

        # evaluate on validation set
        prec1 = 0.0
        lossClassification = 0
        if (epoch + 1) % args.save_freq == 0:
            prec1,prec5,lossClassification = validate(val_loader, model, criterion, epoch)
            writer.add_scalar('data/top1_validation', prec1, epoch)
            writer.add_scalar('data/top3_validation', prec5, epoch)
            writer.add_scalar('data/classification_loss_validation', lossClassification, epoch)
            scheduler.step(lossClassification)
        # remember best prec@1 and save checkpoint
        
        is_best = prec1 >= best_prec1
        best_prec1 = max(prec1, best_prec1)
#        best_in_existing_learning_rate = max(prec1, best_in_existing_learning_rate)
#        
#        if best_in_existing_learning_rate > prec1 + 1:
#            learning_rate_index = learning_rate_index 
#            best_in_existing_learning_rate = 0        

        if (epoch + 1) % args.save_freq == 0:
            checkpoint_name = "%03d_%s" % (epoch + 1, "checkpoint.pth.tar")
            if is_best:
                print("Model son iyi olarak kaydedildi")
                save_checkpoint({
                    'epoch': epoch + 1,
                    'arch': args.arch,
                    'state_dict': model.state_dict(),
                    'best_prec1': best_prec1,
                    'best_loss': best_loss,
                    'optimizer' : optimizer.state_dict(),
                }, is_best, checkpoint_name, saveLocation)
    
    checkpoint_name = "%03d_%s" % (epoch + 1, "checkpoint.pth.tar")
    save_checkpoint({
        'epoch': epoch + 1,
        'arch': args.arch,
        'state_dict': model.state_dict(),
        'best_prec1': best_prec1,
        'best_loss': best_loss,
        'optimizer' : optimizer.state_dict(),
    }, is_best, checkpoint_name, saveLocation)
    writer.export_scalars_to_json("./all_scalars.json")
    writer.close()

def build_model():
    #args.arch：dark_light
    model = models.__dict__[args.arch](num_classes=11, length=args.num_seg, both_flow=args.both_flow)
    
    # if torch.cuda.device_count() > 1:
        # model=torch.nn.DataParallel(model)
    model=torch.nn.DataParallel(model)
    # model = model.cuda()
    model = model.to(device)