# -*- coding: utf-8 -*-
"""
Copyright (c) Yuwei Jin
Created on 2020-12-19 21:39
Written by Yuwei Jin (642281525@qq.com)
"""
import math
import warnings

import torch

from sv.libs.data.dataset.dataset import load_train_data, load_val_data
from sv.libs.core.trainer import MixedPrecisionTrain
from sv.libs.tools import utils


class _Train(MixedPrecisionTrain):
    def __init__(self, cfg, model, optimizer, criterion, evaluator, scheduler):

        model = model.cuda()
        warnings.warn('Note, only single GPU device is supported!')

        self.train_data = load_train_data(cfg)
        self.valid_data = load_val_data(cfg)

        # parse learning rate scheduler
        self.scheduler = utils.parse_lr_scheduler(cfg, optimizer, train_data=self.train_data)
        warnings.warn('Note, only Cosine, Poly, and ExponentialLR scheduler are supported!')

        # some hyper-params
        self.num_class = cfg.DATASET.NUM_CLASS
        self.epochs = cfg.TRAIN.EPOCHS
        self.train_batch_steps = math.floor(len(self.train_data.dataset) / cfg.TRAIN.BATCH_SIZE)
        self.valid_batch_steps = math.floor(len(self.valid_data.dataset) / cfg.TRAIN.BATCH_SIZE)

        self.cfg = cfg

        super().__init__(cfg, model, optimizer, scheduler, criterion, evaluator)

    def _show_logs(self, loss, prob, gt, step, batch_steps, phase='train'):
        conf_mat, acc_dict = self.cal_batch_acc(prob, gt)  # compute confusion matrix, acc, acc dict
        if step % self.cfg.TRAIN.MSG_ITER == 0:
            log_head = "epoch: {}-{} - iter: {}-{} | ".format(self.curr_epoch, self.epochs, step + 1, batch_steps)
            self.print_train_logs(log_head, loss, acc_dict, phase=phase)

        return conf_mat

    def _epoch_train(self):
        self.model.train()
        for i, (im, gt) in enumerate(self.train_data):
            prob, loss = self.forward_backward(im, gt)
            prob = self.get_major_prob(prob)  # multi returns, such as deeply supervision
            conf_mat = self._show_logs(loss, prob, gt, i, self.train_batch_steps)
            self.train_batch_hist += conf_mat

    def _epoch_eval(self):
        self.model.eval()
        with torch.no_grad():
            for i, (im, gt) in enumerate(self.valid_data):
                prob, loss = self.forward(im, gt)
                prob = self.get_major_prob(prob)
                conf_mat = self._show_logs(loss, prob, gt, i, self.valid_batch_steps, 'valid')
                self.valid_batch_hist += conf_mat

    def train(self):
        print("---start training...")
        for epoch in range(self.epochs):
            time_counter = utils.TimeCounter()

            time_counter.tic()
            self._epoch_train()  # call train
            train_time = time_counter.toc()

            time_counter.tic()
            self._epoch_eval()  # call eval

            # calculate epoch accuracy
            self.evaluator.confusion_matrix = self.train_batch_hist
            train_acc, train_logs = self.evaluator.cal_acc(return_acc_dict=True)
            self.evaluator.confusion_matrix = self.valid_batch_hist
            valid_acc, valid_logs = self.evaluator.cal_acc(return_acc_dict=True)

            model_states = {"net": self.model.state_dict(), "optimizer": self.optimizer.state_dict(), "epoch": epoch + 1}
            self.save_checkpoint(model_states)
            valid_time = time_counter.toc()

            # calculate epoch average loss
            train_logs['loss'] = self.train_batch_loss / self.train_batch_steps
            valid_logs['loss'] = self.valid_batch_loss / self.valid_batch_steps
            train_logs['time'] = round(train_time, 2)
            valid_logs['time'] = round(valid_time, 2)

            self.writer.add_scalar('train/epoch_lr', self.get_optimizer_lr(), epoch)
            self.writer.add_scalars('train/time', {'train': train_time, 'val': valid_time}, epoch)
            for key in self.employed_metrics:
                self.writer.add_scalars('train/' + key, {'train': float(train_logs[key]), 'val': float(valid_logs[key])}, epoch)

            self.report_epoch_logs(train_logs, valid_logs)

            self.epoch_update_lr()
            self.epoch_reset()

        self.writer.close()

        print('-------------Congratulations! Training Done!!!-------------')

if __name__ == '__main__':
    from nb_log import LogManager


    class NbLog:
        def __init__(self):
            self.logger = LogManager('simple').get_logger_and_add_handlers(log_path="log 存放地址", log_filename="日志名称")

        def error(self, msg):
            return self.logger.error(msg)

        def debug(self, msg):
            return self.logger.debug(msg)

        def info(self, msg):
            return self.logger.info(msg)

        def warning(self, msg):
            return self.logger.warning(msg)

        def exception(self, msg, exc_info=True):
            return self.logger.exception(msg, exc_info)


    dolog = NbLog()
    dolog.debug("这个是 debug 日志")
    dolog.error("这个是 error 日志")