# -*- coding: UTF-8 -*-
"""
Copyright (c) Yuwei Jin
Created at 2021-07-18 20:53 
Written by Yuwei Jin (642281525@qq.com)
"""
import os
import re

import torch
import numpy as np
from tensorboardX import SummaryWriter
from abc import ABC, abstractmethod
from nb_log import get_logger
from torch.cuda.amp import autocast, GradScaler

from sv.libs.tools import utils

scaler = GradScaler()  # fp-16 training

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def _find_best_value_index(value_list: list, higher_better=True):
    def _sub_func(value: list):
        temp_list = []
        for i, v in enumerate(value_list):
            if v == value:
                temp_list.append(i)
        return temp_list[-1]

    if higher_better:
        max_val = max(value_list)
        return _sub_func(value=max_val)
    else:
        min_val = min(value_list)
        return _sub_func(value=min_val)


class _BaseTrainer(ABC):
    """Base class for trainer"""

    def __init__(self, cfg, model, optimizer, scheduler, criterion, evaluator):
        self.curr_epoch = 1
        self.curr_step = 1
        self.curr_saved_epoch = None

        self.train_batch_loss = 0
        self.valid_batch_loss = 0

        self.key_metric_record = []
        self.last_best_epoch = 0

        self.num_class = cfg.DATASET.NUM_CLASS

        self.train_batch_hist = np.zeros((self.num_class,) * 2)
        self.valid_batch_hist = np.zeros((self.num_class,) * 2)

        self.employed_metrics = ['loss']
        self.employed_metrics.extend(cfg.TRAIN.EMPLOYED_METRICS)

        self.model = model
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.criterion = criterion
        self.evaluator = evaluator

        self.writer = SummaryWriter(cfg.TRAIN.LOGS_SAVE_DIR)

        self.total_time = 0

        self.cfg = cfg

    def epoch_reset(self):
        self.train_batch_hist = np.zeros((self.num_class,) * 2)
        self.valid_batch_hist = np.zeros((self.num_class,) * 2)
        self.train_batch_loss = 0
        self.valid_batch_loss = 0

    def step_update_lr(self):
        """it will update current iterations"""
        c1 = re.search(self.cfg.TRAIN.LR.SCHEDULER, 'Poly', re.IGNORECASE)
        c2 = re.search(self.cfg.TRAIN.LR.SCHEDULER, 'Cosine', re.IGNORECASE)
        if c1 or c2:
            self.scheduler.step()

        self.curr_step += 1

    def epoch_update_lr(self):
        c1 = re.search(self.cfg.TRAIN.LR.SCHEDULER, 'Poly', re.IGNORECASE)
        c2 = re.search(self.cfg.TRAIN.LR.SCHEDULER, 'Cosine', re.IGNORECASE)
        if not c1 and not c2:
            self.scheduler.step()

        self.curr_epoch += 1

    @staticmethod
    def get_major_prob(prob):
        if isinstance(prob, (list, tuple)):  # multi returns, such as deeply supervision
            prob = prob[0]
        return prob

    def get_optimizer_lr(self) -> float:
        """ Get optimizer learning rate """
        return self.optimizer.state_dict()['param_groups'][0]['lr']

    def tensor_to_gpu(self, im, gt):
        im = im.cuda()
        if self.cfg.MODEL.OUTPUT_CHANNELS > 1:  # using softmax, label dim is: B*H*W, sigmoid is: B*1*H*W
            gt = gt.squeeze().long()
        gt = gt.cuda()
        return im, gt

    def cal_batch_acc(self, prob, gt):
        """ cal batch accuracy for each batch during training and validate"""
        pred = utils.tensor_binarize(prob).flatten()  # get binary segmentation results
        mask = utils.tensor_to_numpy(gt).flatten()  # convert cuda tensor to numpy
        hist = utils.fast_hist(input=pred, label=mask, num_class=self.num_class)  # compute confusion matrix
        self.evaluator.confusion_matrix = hist
        _, acc_dict = self.evaluator.cal_acc(return_acc_dict=True)
        return hist, acc_dict

    @staticmethod
    def print_train_logs(log_head: str, loss: float, acc_dict: dict, phase='train'):
        logs = log_head + "loss: {:.6f}".format(loss)
        for key, value in acc_dict.items():
            logs = logs + " - " + key + ": " + str(value).rjust(5, ' ')
        logger = get_logger(phase)
        logger.info(logs)

    def report_epoch_logs(self, train_logs, valid_logs):
        key = self.cfg.TRAIN.KEY_METRIC
        TRAIN = self.cfg.TRAIN
        logger = get_logger('epoch: {}-{} training summary'.format(self.curr_epoch, self.cfg.TRAIN.EPOCHS))
        logger.critical("train - loss: {:.6f} - {}: {} - time: {} min".format(train_logs['loss'], key, train_logs[key], train_logs['time']))
        logger.critical("valid - loss: {:.6f} - {}: {} - time: {} min".format(valid_logs['loss'], key, valid_logs[key], valid_logs['time']))

        self.key_metric_record.append(float(valid_logs[TRAIN.KEY_METRIC]))
        j = _find_best_value_index(self.key_metric_record, TRAIN.HIGHER_BETTER)

        logger = get_logger('epoch: {}-{} training summary'.format(self.curr_epoch, TRAIN.EPOCHS))
        logger.critical('best {} record is at epoch - {}, best record - {:.2f}'.format(key, j + 1, self.key_metric_record[j]))

        t = train_logs['time'] + valid_logs['time']
        self.total_time = self.total_time + t
        remained_epoch = TRAIN.EPOCHS - self.curr_epoch
        remain_time = remained_epoch * t
        logger.warning('elapsed time: {:.2f} hours, {:.2f} hours remains for following training...'.format(
            self.total_time / 60,
            remain_time / 60))
        print('==' * 74)

    def save_checkpoint(self, model_states):
        ckpt = self.cfg.TRAIN.CKPT
        start_save_epoch = ckpt.START_SAVE_EPOCH
        save_path = os.path.join(ckpt.SAVE_DIR, 'ckpt.pth')

        if self.curr_epoch >= start_save_epoch:
            if not ckpt.DELETE_OLD:
                save_path = os.path.join(ckpt.SAVE_DIR, str(self.curr_epoch) + '_' + 'ckpt.pth')
                torch.save(model_states, save_path)
                self.curr_saved_epoch = self.curr_epoch
            else:
                if self.curr_epoch == start_save_epoch:
                    torch.save(model_states, save_path)
                    self.last_best_epoch = self.curr_epoch
                    self.curr_saved_epoch = self.curr_epoch
                else:
                    value = self.key_metric_record[start_save_epoch - 1:]
                    index = _find_best_value_index(value, self.cfg.TRAIN.HIGHER_BETTER)
                    curr_best_epoch = index + start_save_epoch

                    if curr_best_epoch >= self.curr_epoch:
                        os.remove(save_path)
                        torch.save(model_states, save_path)
                        self.last_best_epoch = curr_best_epoch
                        self.curr_saved_epoch = curr_best_epoch

        logger = get_logger('checkpoint saving info')
        print('==' * 74)
        if self.curr_saved_epoch is not None:
            logger.critical('currently saved checkpoint is at epoch - {}'.format(self.curr_saved_epoch))
        else:
            logger.critical('the process of saving model is not started')


class MixedPrecisionTrain(_BaseTrainer):
    def __init__(self, cfg, model, optimizer, scheduler, criterion, evaluator):
        super().__init__(cfg, model, optimizer, scheduler, criterion, evaluator)

    def forward_backward(self, im, gt):
        im, gt = self.tensor_to_gpu(im, gt)
        self.optimizer.zero_grad()  # zero model gradient

        with autocast():  # Runs the forward pass with autocasting.
            prob = self.model(im)
            loss = self.criterion(prob, gt)

            scaler.scale(loss).backward()  # gradient backward
            scaler.step(self.optimizer)  # optimizer parameters
            scaler.update()  # Updates the scale for next iteration.

        self.step_update_lr()  # update learning rate if scheduler is poly, cosine

        self.writer.add_scalar('train/step_lr', self.get_optimizer_lr(), self.curr_step)

        loss = loss.item()
        self.train_batch_loss += loss

        return prob, loss

    def forward(self, im, gt):
        """
        Return:
            prob: model prediction
            loss: loss value (not Tensor)
        """
        im, gt = self.tensor_to_gpu(im, gt)
        with autocast():  # Runs the forward pass with autocasting.
            prob = self.model(im)
            loss = self.criterion(prob, gt)

        loss = loss.item()
        self.valid_batch_loss += loss

        return prob, loss


class NormalTrain(_BaseTrainer):
    def __init__(self, cfg, model, optimizer, scheduler, criterion, evaluator):
        super().__init__(cfg, model, optimizer, scheduler, criterion, evaluator)

    def forward_backward(self, im, gt):
        im, gt = self.tensor_to_gpu(im, gt)

        self.optimizer.zero_grad()  # zero model gradient

        prob = self.model(im)
        loss = self.criterion(prob, gt)
        loss.backward()  # gradient backward
        self.optimizer.step()  # optimizer parameters

        self.step_update_lr()  # update learning rate if scheduler is poly, cosine

        loss = loss.item()
        self.train_batch_loss += loss

        return prob, loss

    def forward(self, im, gt):
        """
        Return:
            prob: model prediction
            loss: loss value (not Tensor)
        """
        im, gt = self.tensor_to_gpu(im, gt)
        prob = self.model(im)
        loss = self.criterion(prob, gt)

        loss = loss.item()
        self.valid_batch_loss += loss

        return prob, loss
