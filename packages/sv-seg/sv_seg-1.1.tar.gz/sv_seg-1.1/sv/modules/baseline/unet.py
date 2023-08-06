# -*- coding: UTF-8 -*-
"""
Copyright (c) Yuwei Jin
Created at 2021-10-24 17:03 
Written by Yuwei Jin (642281525@qq.com)
"""

import torch
import torch.nn as nn

from sv.modules.seg_modules import UNetEncBlock, Bottleneck, DoubleConv, UNetDecBlock, Classifier, upsample
from sv.modules.backbones.resnet.ori_resnet import resnet18

supported_encoder = ['naive', 'resnet-18d', 'resnet-18', 'vgg-16', 'resnet-34', 'resnet-50', 'resnet-101']


class _NaiveUNetEnc(nn.Module):
    def __init__(self):
        super(_NaiveUNetEnc, self).__init__()
        self.enc1 = UNetEncBlock(3, 64)
        self.enc2 = UNetEncBlock(64, 128)
        self.enc3 = UNetEncBlock(128, 256)
        self.enc4 = UNetEncBlock(256, 512)
        self.bridge_conv = DoubleConv(512, 1024)

    def forward(self, x):
        x1 = self.enc1(x)
        x2 = self.enc2(x1[1])
        x3 = self.enc3(x2[1])
        x4 = self.enc4(x3[1])
        x5 = self.bridge_conv(x4[1])
        return x1[0], x2[0], x3[0], x4[0], x5


class _UNetDec(nn.Module):
    def __init__(self, num_class, in_chs_list=[64, 128, 256, 512, 1024], use_ds=False):
        super(_UNetDec, self).__init__()

        self.dec = nn.ModuleList()

        for i in range(len(in_chs_list) -1, 0, -1):
            m = UNetDecBlock(in_chs_list[i-1], in_chs_list[i])
            self.dec.append(m)

        self.cls = Classifier(in_chs_list[0], num_class)

    def forward(self, feats):
        feats = list(feats)
        feats.reverse()
        for i, m in enumerate(self.dec):
            low_f = feats[i+1]
            if i == 0:
                x = m(low_f, feats[i])
            else:
                x = m(low_f, x)

        p = self.cls(x)

        return p


class UNet(nn.Module):
    def __init__(self, num_class=1, encoder_type='naive'):
        super().__init__()

        if encoder_type not in supported_encoder:
            raise ValueError('encoder type is not supported. Got {}'.format(encoder_type))

        if encoder_type == 'naive':
            self.encoder = _NaiveUNetEnc()
            self.decoder = _UNetDec(num_class, [64, 128, 256, 512, 1024])

        if encoder_type == 'resnet-18':
            self.encoder = resnet18(pretrained=True)
            self.decoder = _UNetDec(num_class, [64, 128, 256, 512])

    def forward(self, x):
        feats = self.encoder(x)
        p = self.decoder(feats)
        p = upsample(p, x.size()[2:])
        return p


if __name__ == '__main__':
    model = UNet(encoder_type='resnet-18').eval()
    x = torch.randn(1, 3, 512, 512)
    print(model(x).size())
