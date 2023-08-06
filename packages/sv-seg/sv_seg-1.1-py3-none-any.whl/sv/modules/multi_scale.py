# -*- coding: UTF-8 -*-
"""
Copyright (c) Yuwei Jin
Created at 2021-10-23 19:16 
Written by Yuwei Jin (642281525@qq.com)
"""
import torch
from torch import nn
from torch.nn import functional as F

from sv.libs.tools.init_weight import init_weights
from sv.modules.packaged_conv import Conv3x3_BN_ReLU, Conv1x1_BN_ReLU


class AtrousPyramidPooling(nn.Module):
    """ASPP: ref DeepLab v3+"""
    def __init__(self, in_chs, reduction_dim=256, rates=(1, 6, 12, 18)):
        super(AtrousPyramidPooling, self).__init__()

        self.pool = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            Conv1x1_BN_ReLU(in_chs, reduction_dim)
        )

        self.conv1 = Conv3x3_BN_ReLU(in_chs, reduction_dim, dilation=rates[0])
        self.conv2 = Conv3x3_BN_ReLU(in_chs, reduction_dim, dilation=rates[1])
        self.conv3 = Conv3x3_BN_ReLU(in_chs, reduction_dim, dilation=rates[2])
        self.conv4 = Conv3x3_BN_ReLU(in_chs, reduction_dim, dilation=rates[3])

        self.bottle_conv = nn.Sequential(
            Conv1x1_BN_ReLU(5 * reduction_dim, reduction_dim),
            nn.Dropout2d(p=0.2)
        )

    def forward(self, x):
        pool = self.pool(x)
        pool = F.upsample(input=pool, size=x.size()[2:], mode='bilinear', align_corners=True)

        x1 = self.conv1(x)
        x2 = self.conv2(x)
        x3 = self.conv3(x)
        x4 = self.conv4(x)

        x = torch.cat([pool, x1, x2, x3, x4], dim=1)

        return self.bottle_conv(x)


class PPM(nn.Module):
    """Pyramid Pooling Module: ref PSPNet"""
    def __init__(self, in_chs, reduction_dim, out_chs, bins=(1, 2, 3, 6)):
        super().__init__()
        self.stages = nn.ModuleList([self._make_stage(in_chs, reduction_dim, b) for b in bins])

        self.bottle_conv = nn.Sequential(
            nn.Conv2d(in_chs * 2, out_chs, kernel_size=1, bias=False),
            nn.BatchNorm2d(out_chs),
            nn.ReLU(inplace=True),
            nn.Dropout2d(p=0.2)
        )

        init_weights(self.stages, self.bottle_conv)

    @staticmethod
    def _make_stage(in_chs, reduction_dim, bin):
        return nn.Sequential(
            nn.AdaptiveAvgPool2d(bin),
            nn.Conv2d(in_chs, reduction_dim, kernel_size=1, bias=False),
            nn.BatchNorm2d(reduction_dim),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        H, W = x.size()[2:]

        out = x
        for f in self.stages:
            y = f(x)
            y = F.interpolate(input=y, size=(H, W), mode='bilinear', align_corners=True)
            out = torch.cat([out, y], dim=1)

        return self.bottle_conv(out)


class FPA(nn.Module):
    def __init__(self, channels=2048):
        """
        Feature Pyramid Attention
        :type channels: int
        """
        super(FPA, self).__init__()
        channels_mid = int(channels/4)

        self.channels_cond = channels

        # Master branch
        self.conv_master = nn.Conv2d(self.channels_cond, channels, kernel_size=1, bias=False)
        self.bn_master = nn.BatchNorm2d(channels)

        # Global pooling branch
        self.conv_gpb = nn.Conv2d(self.channels_cond, channels, kernel_size=1, bias=False)
        self.bn_gpb = nn.BatchNorm2d(channels)

        # C333 because of the shape of last feature maps is (16, 16).
        self.conv7x7_1 = nn.Conv2d(self.channels_cond, channels_mid, kernel_size=(7, 7), stride=2, padding=3, bias=False)
        self.bn1_1 = nn.BatchNorm2d(channels_mid)
        self.conv5x5_1 = nn.Conv2d(channels_mid, channels_mid, kernel_size=(5, 5), stride=2, padding=2, bias=False)
        self.bn2_1 = nn.BatchNorm2d(channels_mid)
        self.conv3x3_1 = nn.Conv2d(channels_mid, channels_mid, kernel_size=(3, 3), stride=2, padding=1, bias=False)
        self.bn3_1 = nn.BatchNorm2d(channels_mid)

        self.conv7x7_2 = nn.Conv2d(channels_mid, channels_mid, kernel_size=(7, 7), stride=1, padding=3, bias=False)
        self.bn1_2 = nn.BatchNorm2d(channels_mid)
        self.conv5x5_2 = nn.Conv2d(channels_mid, channels_mid, kernel_size=(5, 5), stride=1, padding=2, bias=False)
        self.bn2_2 = nn.BatchNorm2d(channels_mid)
        self.conv3x3_2 = nn.Conv2d(channels_mid, channels_mid, kernel_size=(3, 3), stride=1, padding=1, bias=False)
        self.bn3_2 = nn.BatchNorm2d(channels_mid)

        # Convolution Upsample
        self.conv_upsample_3 = nn.ConvTranspose2d(channels_mid, channels_mid, kernel_size=4, stride=2, padding=1, bias=False)
        self.bn_upsample_3 = nn.BatchNorm2d(channels_mid)

        self.conv_upsample_2 = nn.ConvTranspose2d(channels_mid, channels_mid, kernel_size=4, stride=2, padding=1, bias=False)
        self.bn_upsample_2 = nn.BatchNorm2d(channels_mid)

        self.conv_upsample_1 = nn.ConvTranspose2d(channels_mid, channels, kernel_size=4, stride=2, padding=1, bias=False)
        self.bn_upsample_1 = nn.BatchNorm2d(channels)

        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        """
        :param x: Shape: [b, 2048, h, w]
        :return: out: Feature maps. Shape: [b, 2048, h, w]
        """
        # Master branch
        x_master = self.conv_master(x)
        x_master = self.bn_master(x_master)

        # Global pooling branch
        x_gpb = nn.AvgPool2d(x.shape[2:])(x).view(x.shape[0], self.channels_cond, 1, 1)
        x_gpb = self.conv_gpb(x_gpb)
        x_gpb = self.bn_gpb(x_gpb)

        # Branch 1
        x1_1 = self.conv7x7_1(x)
        x1_1 = self.bn1_1(x1_1)
        x1_1 = self.relu(x1_1)
        x1_2 = self.conv7x7_2(x1_1)
        x1_2 = self.bn1_2(x1_2)

        # Branch 2
        x2_1 = self.conv5x5_1(x1_1)
        x2_1 = self.bn2_1(x2_1)
        x2_1 = self.relu(x2_1)
        x2_2 = self.conv5x5_2(x2_1)
        x2_2 = self.bn2_2(x2_2)

        # Branch 3
        x3_1 = self.conv3x3_1(x2_1)
        x3_1 = self.bn3_1(x3_1)
        x3_1 = self.relu(x3_1)
        x3_2 = self.conv3x3_2(x3_1)
        x3_2 = self.bn3_2(x3_2)

        # Merge branch 1 and 2
        x3_upsample = self.relu(self.bn_upsample_3(self.conv_upsample_3(x3_2)))
        x2_merge = self.relu(x2_2 + x3_upsample)
        x2_upsample = self.relu(self.bn_upsample_2(self.conv_upsample_2(x2_merge)))
        x1_merge = self.relu(x1_2 + x2_upsample)

        x_master = x_master * self.relu(self.bn_upsample_1(self.conv_upsample_1(x1_merge)))

        #
        out = self.relu(x_master + x_gpb)

        return out
