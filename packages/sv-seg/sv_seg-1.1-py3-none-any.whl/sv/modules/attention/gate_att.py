# -*- coding: UTF-8 -*-
"""
Copyright (c) Yuwei Jin
Created at 2021-10-23 18:29 
Written by Yuwei Jin (642281525@qq.com)
"""
import torch
from torch import nn

from sv.libs.tools.init_weight import init_weights


class CrossLevelGate(nn.Module):
    def __init__(self, in_chs):
        super().__init__()
        self.gate = nn.Sequential(
            nn.Conv2d(in_chs, 1, kernel_size=1),
            nn.Sigmoid()
        )
        self.gamma = nn.Parameter(torch.ones(1))

        init_weights(self.gate)

    def forward(self, low_f, high_f):
        x = torch.cat([low_f, high_f], dim=1)
        out = self.gate(x) * self.gamma * low_f
        return out