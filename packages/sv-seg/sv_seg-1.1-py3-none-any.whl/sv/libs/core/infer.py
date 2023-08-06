# -*- coding: UTF-8 -*-
"""
Copyright (c) Yuwei Jin
Created at 2021-07-19 14:38
Written by Yuwei Jin (642281525@qq.com)
"""
import os
import numpy as np
import torch
from abc import ABC, abstractmethod
from torch.cuda.amp import autocast
from torchvision.transforms.functional import vflip, hflip
from torch.nn import functional as F


def resize_tensor(input, size, resize_mode='bilinear'):
    if not isinstance(input, torch.Tensor):
        raise ValueError('Input should be torch.Tensor type. Got unexpected type:{}'.format(type(input)))

    if resize_mode == 'bilinear':
        out = F.interpolate(input, size=size, mode=resize_mode, align_corners=True)
    elif resize_mode == 'nearset':
        out = F.interpolate(input, size=size, mode=resize_mode)
    else:
        raise NotImplementedError()

    return out


class Infer(ABC):
    def __init__(self, model, cfg):
        model = model().cuda()
        try:
            ckpt_path = os.path.join(cfg.TRAIN.CKPT.SAVE_DIR, 'ckpt.pth')
            weight = torch.load(ckpt_path)['net']
            model.load_state_dict(weight)
        except FileNotFoundError:
            raise FileNotFoundError('saved model weight is not found in dir: {}'.format(cfg.TRAIN.CKPT.SAVE_DIR))
        self.model = model.eval()
        num_class = cfg.DATASET.NUM_CLASS
        self.conf_mat = np.zeros((num_class, num_class))
        self.cfg = cfg

    def _infer(self, im: torch.Tensor) -> torch.Tensor:
        im = im.cuda()
        if self.cfg.TEST.H_FLIP and self.cfg.TEST.V_FLIP:
            x = torch.cat([im, hflip(im)], dim=0)
            x = torch.cat([x, vflip(im)], dim=0)
            y = self.model(x)
            out = y[0, :, :, :] + hflip(y[1, :, :, :]) + vflip(y[2, :, :, :])
            return out.unsqueeze(dim=0) / 3.0
        elif self.cfg.TEST.H_FLIP and not self.cfg.TEST.V_FLIP:
            x = torch.cat([im, hflip(im)], dim=0)
            y = self.model(x)
            out = y[0, :, :, :] + hflip(y[1, :, :, :])
            return out.unsqueeze(dim=0) / 2.0
        elif not self.cfg.TEST.H_FLIP and self.cfg.TEST.V_FLIP:
            x = torch.cat([im, vflip(im)], dim=0)
            y = self.model(x)
            out = y[0, :, :, :] + vflip(y[1, :, :, :])
            return out.unsqueeze(dim=0) / 2.0
        else:
            return self.model(im)

    def _multi_scale_infer(self, im: torch.Tensor) -> torch.Tensor:
        """ multi scale inference """
        _, _, ori_h, ori_w = im.size()
        final_prob = torch.zeros([1, self.cfg.MODEL.OUTPUT_CHANNELS, ori_h, ori_w]).cuda()

        for scale in self.cfg.TEST.MS_SCALE_LIST:
            new_h = int(ori_h * scale)
            new_w = int(ori_w * scale)
            new_im = resize_tensor(input=im, size=[new_h, new_w])

            prob = self._infer(new_im)
            prob = resize_tensor(prob, (ori_h, ori_w))
            final_prob += prob

        final_prob /= len(self.cfg.TEST.MS_SCALE_LIST)

        return final_prob

    def forward(self, x):
        if self.cfg.TEST.MS:
            out = self._multi_scale_infer(x)
        else:
            out = self._infer(x)
        return out
