# -*- coding: UTF-8 -*-
"""
Copyright (c) Yuwei Jin
Created at 2021-06-11 15:36
Written by Yuwei Jin (642281525@qq.com)
"""
import os
import warnings
import cv2
import torch
import random
import numpy as np

from torch.utils.data.dataloader import DataLoader
from torch.utils.data.dataset import Dataset

from sv.libs.data.dataset import joint_transforms
from sv.libs.tools import utils


def _parse_train_aug_method(cfg, mean):
    aug = cfg.TRAIN.AUG
    out = []
    if aug.MULTI_SCALE:
        out.append(joint_transforms.RandomScale(cfg))

    out.append(joint_transforms.RandomCrop(cfg, mean))

    if aug.FLIP:
        out.append(joint_transforms.RandomFlip(cfg))
    if aug.ROTATION:
        out.append(joint_transforms.RandomRotation(cfg))
    if aug.COLOR_JITTER:
        out.append(joint_transforms.RandomColorJitter(cfg))
    if aug.GAUSSIAN_BLUR:
        out.append(joint_transforms.RandomGaussianBlur(cfg))
    if aug.GAUSSIAN_NOISE:
        out.append(joint_transforms.RandomGaussianNoise(cfg))
    return out


def _read_image(im_src, gt_src, gt_normalize=True):
    """ for two-class semantic segmentation task, set gt_normalize=True"""
    im = cv2.imread(im_src)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB) / 255.0
    gt = cv2.imread(gt_src, cv2.IMREAD_GRAYSCALE)

    if gt_normalize:
        gt /= 255

    return im, gt


class _TrainValTestDataset(Dataset):
    def __init__(self, cfg, training=True, test=False):

        if cfg.DATASET.NUM_CLASS > 2:
            warnings.warn('the label will be normalized to {0, 1}')

        # load mean_std
        mean, std = utils.load_mean_std(cfg)

        # define data augmentation transformation
        temp = joint_transforms.Normalize(mean, std)
        if training:
            transforms = _parse_train_aug_method(cfg, mean)
            transforms.append(temp)
        else:
            transforms = [temp]
        self.transforms = joint_transforms.Compose(transforms)

        # define data set dir
        if training and test:  # validation phase
            dataset_dir = cfg.DATASET.VALID_SET
        elif training and not test:  # training phase
            dataset_dir = cfg.DATASET.TRAIN_SET
        else:
            dataset_dir = cfg.DATASET.TEST_SET

        # generate samples
        self.samples = self._make_samples(dataset_dir=dataset_dir)

        self.test = test
        self.cfg = cfg

    def _make_samples(self, dataset_dir):
        im_dir = os.path.join(dataset_dir, 'image')
        gt_dir = os.path.join(dataset_dir, 'label')

        samples = []
        for f in os.listdir(im_dir):
            if f.endswith(self.cfg.DATASET.IMG_EXTENSION):
                im = os.path.join(im_dir, f)
                gt = os.path.join(gt_dir, f)
                samples.append((im, gt))

        if len(samples) == 0:
            raise FileNotFoundError('None of image sample is found.')

        return samples

    def __getitem__(self, index):
        im_src, gt_src = self.samples[index]

        im, gt = _read_image(im_src, gt_src)

        if self.test:
            f = im_src.split('/')
            im_name = f[-1]
            im, gt = self.transforms(im, gt)
            return im_name, im, gt
        else:
            im, gt = self.transforms(im, gt)
            return im, gt

    def __len__(self):
        return len(self.samples)


def _seed_worker(worker_id):
    worker_seed = torch.initial_seed() % 2 ** 32
    np.random.seed(worker_seed)
    random.seed(worker_seed)


def load_train_data(cfg):
    dataset = _TrainValTestDataset(cfg, training=True, test=False)

    time_counter = utils.TimeCounter(return_sec=True)
    time_counter.tic()
    data = DataLoader(
        dataset=dataset,
        batch_size=cfg.TRAIN.BATCH_SIZE,
        shuffle=True,
        drop_last=cfg.DATALOADER.DROP_LAST,
        num_workers=cfg.DATALOADER.WORKERS,
        pin_memory=cfg.DATALOADER.PIP_MEMORY,
        worker_init_fn=_seed_worker
    )
    t = time_counter.toc()

    print('{} training images were loaded from dir:{}'.format(dataset.__len__(), cfg.DATASET.TRAIN_SET))
    print('elapsed time for loading training set is {} seconds'.format(t))

    return data


def load_val_data(cfg):
    dataset = _TrainValTestDataset(cfg, training=False, test=False)

    time_counter = utils.TimeCounter(return_sec=True)
    time_counter.tic()
    data = DataLoader(
        dataset=dataset,
        batch_size=cfg.TRAIN.BATCH_SIZE,
        shuffle=True,
        num_workers=cfg.DATALOADER.WORKERS,
        drop_last=True,
        pin_memory=True
    )
    t = time_counter.toc()

    print('{} validate images were loaded from dir:{}'.format(dataset.__len__(), cfg.DATASET.VALID_SET))
    print('elapsed time for loading validate set is {} seconds'.format(t))

    return data


def load_test_data(cfg):
    dataset = _TrainValTestDataset(cfg, training=False, test=True)

    time_counter = utils.TimeCounter(return_sec=True)
    time_counter.tic()
    data = DataLoader(
        dataset=dataset,
        batch_size=1,
        shuffle=False,
        num_workers=1,
        drop_last=False,
        pin_memory=True
    )

    t = time_counter.toc()

    print('{} test images were loaded from dir:{}'.format(dataset.__len__(), cfg.DATASET.VALID_SET))
    print('elapsed time for loading test set is {} seconds'.format(t))

    return data
