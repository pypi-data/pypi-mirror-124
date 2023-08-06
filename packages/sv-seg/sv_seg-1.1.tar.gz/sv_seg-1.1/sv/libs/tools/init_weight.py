# -*- coding: UTF-8 -*-
"""
Copyright (c) Yuwei Jin
Created at 2021-05-04 15:28
Written by Yuwei Jin (642281525@qq.com)
"""

import torch.nn as nn


def _real_init_weights(m, nonlinearity='relu'):
    if isinstance(m, list):
        for mini_m in m:
            _real_init_weights(mini_m)
    else:
        if isinstance(m, nn.Conv2d):
            # print('initializing Convolution layer...')
            nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity=nonlinearity)
            if m.bias is not None:
                nn.init.zeros_(m.bias)
        elif isinstance(m, (nn.BatchNorm2d, nn.GroupNorm, nn.InstanceNorm2d)):
            # print('initializing BN layer...')
            nn.init.ones_(m.weight)
            if m.bias is not None:
                nn.init.zeros_(m.bias)
        elif isinstance(m, nn.Linear):
            # print('initializing Linear layer...')
            nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity=nonlinearity)
            if m.bias is not None:
                nn.init.zeros_(m.bias)
        elif isinstance(m, nn.Module):
            for mini_m in m.children():
                _real_init_weights(mini_m)
        else:
            raise NotImplementedError('Unknown init module.')


def init_weights(*models, nonlinearity='relu'):
    """
    Initialize model's modules.
    """
    print('initializing modules...')
    for model in models:
        _real_init_weights(model, nonlinearity=nonlinearity)