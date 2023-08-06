# -*- coding: UTF-8 -*-
"""
Copyright (c) Yuwei Jin
Created at 2021-10-23 17:20 
Written by Yuwei Jin (642281525@qq.com)
"""
import torch
import torch.nn as nn

from sv.libs.tools.init_weight import init_weights


# ------ 3x3 Conv -----
class Conv3x3(nn.Module):
    def __init__(self, in_chs, out_chs, stride=1, dilation=1, groups=1, bias=True):
        super(Conv3x3, self).__init__()
        self.conv = nn.Conv2d(in_chs, out_chs, kernel_size=3, padding=dilation, stride=stride, dilation=dilation, groups=groups, bias=bias)
        init_weights(self.conv)

    def forward(self, x):
        out = self.conv(x)
        return out


# ------ 3x3 Conv + BN + ReLU ------
class Conv3x3_BN_ReLU(nn.Module):
    def __init__(self, in_chs, out_chs, stride=1, padding=1, dilation=1, groups=1, bn_momentum=0.1):
        super(Conv3x3_BN_ReLU, self).__init__()

        if dilation > 1:
            padding = dilation

        self.conv = nn.Sequential(
            nn.Conv2d(in_chs, out_chs, kernel_size=3, stride=stride, padding=padding, dilation=dilation,
                      groups=groups, bias=False),
            nn.BatchNorm2d(out_chs, momentum=bn_momentum),
            nn.ReLU(inplace=True)
        )

        init_weights(self.conv)

    def forward(self, x):
        return self.conv(x)


class Conv3x3_BN_PReLU(nn.Module):
    def __init__(self, in_chs, out_chs, stride=1, padding=1, dilation=1, groups=1, bn_momentum=0.1):
        super().__init__()

        if dilation > 1:
            padding = dilation

        self.conv = nn.Sequential(
            nn.Conv2d(in_chs, out_chs, kernel_size=3, stride=stride, padding=padding, dilation=dilation,
                      groups=groups, bias=False),
            nn.BatchNorm2d(out_chs, momentum=bn_momentum),
            nn.PReLU()
        )

        init_weights(self.conv)

    def forward(self, x):
        return self.conv(x)

class Conv3x3_BN_LeakyReLU(nn.Module):
    def __init__(self, in_chs, out_chs, stride=1, padding=1, dilation=1, groups=1, bn_momentum=0.1, negative_slope=0.1):
        super().__init__()

        if dilation > 1:
            padding = dilation

        self.conv = nn.Sequential(
            nn.Conv2d(in_chs, out_chs, kernel_size=3, stride=stride, padding=padding, dilation=dilation,
                      groups=groups, bias=False),
            nn.BatchNorm2d(out_chs, momentum=bn_momentum),
            nn.LeakyReLU(negative_slope=negative_slope, inplace=True)
        )

        init_weights(self.conv, nonlinearity='leakyrelu')

    def forward(self, x):
        return self.conv(x)


class BN_ReLU_Conv3x3(nn.Module):
    """ pre-activate """

    def __init__(self, in_chs, out_chs, stride=1, padding=1, dilation=1, groups=1, momentum=0.1):
        super(BN_ReLU_Conv3x3, self).__init__()

        self.conv = nn.Sequential(
            nn.BatchNorm2d(in_chs, momentum=momentum),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_chs, out_chs, kernel_size=3, stride=stride, padding=padding, dilation=dilation, groups=groups, bias=False)
        )

        init_weights(self.conv)

    def forward(self, x):
        return self.conv(x)


# ----- Conv 1x1 -----
class Conv1x1(nn.Module):
    def __init__(self, in_chs, out_chs, stride=1, groups=1, bias=True):
        super(Conv1x1, self).__init__()
        self.conv = nn.Conv2d(in_chs, out_chs, kernel_size=1, stride=stride, groups=groups, bias=bias)

        init_weights(self.conv)

    def forward(self, x):
        out = self.conv(x)
        return out


class Conv1x1_BN_ReLU(nn.Module):
    def __init__(self, in_chs, out_chs, groups=1, bn_momentum=0.1):
        super(Conv1x1_BN_ReLU, self).__init__()

        self.conv = nn.Sequential(
            nn.Conv2d(in_chs, out_chs, kernel_size=1, groups=groups, bias=False),
            nn.BatchNorm2d(out_chs, momentum=bn_momentum),
            nn.ReLU(inplace=True)
        )
        init_weights(self.conv)

    def forward(self, x):
        return self.conv(x)


class Conv1x1_BN_PReLU(nn.Module):
    def __init__(self, in_chs, out_chs, groups=1, bn_momentum=0.1):
        super().__init__()

        self.conv = nn.Sequential(
            nn.Conv2d(in_chs, out_chs, kernel_size=1, groups=groups, bias=False),
            nn.BatchNorm2d(out_chs, momentum=bn_momentum),
            nn.PReLU()
        )
        init_weights(self.conv)

    def forward(self, x):
        return self.conv(x)


class Conv1x1_BN_LeakyReLU(nn.Module):
    def __init__(self, in_chs, out_chs, groups=1, bn_momentum=0.1):
        super().__init__()

        self.conv = nn.Sequential(
            nn.Conv2d(in_chs, out_chs, kernel_size=1, groups=groups, bias=False),
            nn.BatchNorm2d(out_chs, momentum=bn_momentum),
            nn.PReLU()
        )
        init_weights(self.conv, nonlinearity='leakyrelu')

    def forward(self, x):
        return self.conv(x)


class BN_ReLU_Conv1x1(nn.Module):
    """ pre-activate """

    def __init__(self, in_chs, out_chs, stride=1, dilation=1, groups=1, momentum=0.1):
        super(BN_ReLU_Conv1x1, self).__init__()

        self.conv = nn.Sequential(
            nn.BatchNorm2d(in_chs, momentum=momentum),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_chs, out_chs, kernel_size=1, stride=stride, dilation=dilation, groups=groups, bias=False)
        )

        init_weights(self.conv)

    def forward(self, x):
        return self.conv(x)


class ConvBNReLU(nn.Module):
    def __init__(self, in_chan, out_chan, ks=3, stride=1, padding=1, *args, **kwargs):
        super(ConvBNReLU, self).__init__()
        self.conv = nn.Conv2d(in_chan, out_chan, kernel_size=ks, stride=stride, padding=padding, bias=False)
        # self.bn = BatchNorm2d(out_chan)
        self.bn = nn.BatchNorm2d(out_chan)
        self.relu = nn.ReLU()

        init_weights(self.conv, self.bn)

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)
        return x



class DWConv(nn.Module):
    """Depthwise-separable convolution"""

    def __init__(self, in_chs, out_chs, dilation=1, relu=True):
        super(DWConv, self).__init__()

        self.depth_conv = nn.Sequential(
            nn.Conv2d(in_chs, in_chs, kernel_size=3, groups=in_chs, padding=dilation, dilation=dilation, bias=False),
            nn.BatchNorm2d(in_chs)
        )

        self.point_conv = nn.Sequential(
            nn.Conv2d(in_chs, out_chs, kernel_size=1, bias=False),
            nn.BatchNorm2d(out_chs)
        )

        self.relu = relu

        init_weights(self.point_conv, self.depth_conv)

    def forward(self, x):
        out = self.depth_conv(x)
        out = self.point_conv(out)

        if self.relu:
            out = torch.relu(out)

        return out