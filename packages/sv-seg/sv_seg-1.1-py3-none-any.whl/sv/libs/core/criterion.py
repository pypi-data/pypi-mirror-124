# -*- coding: UTF-8 -*-
"""
Copyright (c) Yuwei Jin
Created at 2021-07-15 09:09 
Written by Yuwei Jin (642281525@qq.com)
"""
import math

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable


# from libs.functional import edge_extraction


class BinaryDiceLoss(nn.Module):
    """Dice loss of binary class
        Args:
            smooth: A float number to smooth loss, and avoid NaN error, default: 1
            p: Denominator value: \sum{x^p} + \sum{y^p}, default: 2
            predict: A tensor of shape [N, *]
            target: A tensor of shape same with predict
            reduction: Reduction method to apply, return mean over batch if 'mean',
                return sum if 'sum', return a tensor of shape [N,] if 'none'
        Returns:
            Loss tensor according to arg reduction
        Raise:
            Exception if unexpected reduction
        """

    def __init__(self, smooth=1., p=2, reduction='mean'):
        super(BinaryDiceLoss, self).__init__()
        self.smooth = smooth
        self.p = p
        self.reduction = reduction

    def forward(self, input, target):
        assert input.shape[0] == target.shape[0], "predict & target batch size don't match"

        input = torch.sigmoid(input)

        n = input.size()[0]

        prob = input.view(n, -1)
        mask = target.view(n, -1)
        intersection = (prob * mask).sum(1)
        loss = 1 - ((2. * intersection + self.smooth) / (prob.sum(1) + mask.sum(1) + self.smooth))

        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        elif self.reduction == 'none':
            return loss
        else:
            raise Exception('Unexpected reduction {}'.format(self.reduction))


class BCEDiceLoss(nn.Module):
    def __init__(self, dice_weight=1.0):
        super(BCEDiceLoss, self).__init__()
        self.bce = nn.BCEWithLogitsLoss()
        self.dice = BinaryDiceLoss()
        self.dice_weight = dice_weight

    def forward(self, x, y) -> torch.Tensor:
        """
        :param x: model predictions
        :param y: label
        :return: loss
        """
        t = torch.sigmoid(x)

        loss = self.bce(x, y) + self.dice_weight * self.dice(t, y)

        return loss


class OHEM_CELoss(nn.Module):
    """OHEM Cross entropy loss"""

    def __init__(self, ignore_index: int = -1, thresh: float = 0.7, min_kept: int = 100000):
        super(OHEM_CELoss, self).__init__()

        self.ignore_index = ignore_index
        self.thresh = thresh
        self.min_kept = min_kept

    def forward(self, y_pred, y_true):
        # y_pred: [N, C, H, W]
        # y_true: [N, H, W]
        # seg_weight: [N, H, W]
        y_true = y_true.unsqueeze(1)
        with torch.no_grad():
            assert y_pred.shape[2:] == y_true.shape[2:]
            assert y_true.shape[1] == 1
            seg_label = y_true.squeeze(1).long()
            batch_kept = self.min_kept * seg_label.size(0)
            valid_mask = seg_label != self.ignore_index
            seg_weight = y_pred.new_zeros(size=seg_label.size())
            valid_seg_weight = seg_weight[valid_mask]

            seg_prob = F.softmax(y_pred, dim=1)

            tmp_seg_label = seg_label.clone().unsqueeze(1)
            tmp_seg_label[tmp_seg_label == self.ignore_index] = 0
            seg_prob = seg_prob.gather(1, tmp_seg_label).squeeze(1)
            sort_prob, sort_indices = seg_prob[valid_mask].sort()

            if sort_prob.numel() > 0:
                min_threshold = sort_prob[min(batch_kept,
                                              sort_prob.numel() - 1)]
            else:
                min_threshold = 0.0
            threshold = max(min_threshold, self.thresh)
            valid_seg_weight[seg_prob[valid_mask] < threshold] = 1.

            seg_weight[valid_mask] = valid_seg_weight

            losses = F.cross_entropy(y_pred, y_true.squeeze(1), ignore_index=self.ignore_index, reduction='none')
            losses = losses * seg_weight

            return losses.sum() / seg_weight.sum()


def _masked_ignore(y_pred: torch.Tensor, y_true: torch.Tensor, ignore_index: int):
    # usually used for BCE-like loss
    y_pred = y_pred.reshape((-1,))
    y_true = y_true.reshape((-1,))
    valid = y_true != ignore_index
    y_true = y_true.masked_select(valid).float()
    y_pred = y_pred.masked_select(valid).float()
    return y_pred, y_true


class LabelSmoothingCELoss(nn.Module):
    def __init__(self, eps: float = 0.1, reduction: str = 'mean', ignore_index: int = -1):
        super(LabelSmoothingCELoss, self).__init__()
        self.eps = eps
        self.reduction = reduction
        self.ignore_index = ignore_index

    def forward(self, output: torch.Tensor, target: torch.Tensor):
        c = output.size()[0]
        log_preds = F.log_softmax(output, dim=1)

        loss = -log_preds.sum(dim=1)

        loss, _ = _masked_ignore(loss, target, self.ignore_index)

        if self.reduction == 'sum':
            loss = loss.sum()
        elif self.reduction == 'mean':
            loss = loss.mean()

        nll_loss = F.nll_loss(log_preds, target, reduction=self.reduction, ignore_index=self.ignore_index)
        loss = loss * self.eps / c + (1 - self.eps) * nll_loss

        return loss


def label_smoothing_binary_cross_entropy(output: torch.Tensor, target: torch.Tensor, eps: float = 0.1,
                                         reduction: str = 'mean', ignore_index: int = 255):
    output, target = _masked_ignore(output, target, ignore_index)
    target = torch.where(target == 0, target + eps, target - eps)
    return F.binary_cross_entropy_with_logits(output, target, reduction=reduction)


def binary_cross_entropy_with_logits(output: torch.Tensor, target: torch.Tensor, reduction: str = 'mean',
                                     ignore_index: int = 255):
    output, target = _masked_ignore(output, target, ignore_index)
    return F.binary_cross_entropy_with_logits(output, target, reduction=reduction)


@torch.jit.script
def online_hard_example_mining(losses: torch.Tensor, keep_ratio: float):
    assert 0 < keep_ratio < 1, 'The value of keep_ratio must be from 0 to 1.'
    # 1. keep num
    num_inst = losses.numel()
    num_hns = int(keep_ratio * num_inst)
    # 2. select loss
    top_loss, _ = losses.reshape(-1).topk(num_hns, -1)
    loss_mask = (top_loss != 0)
    # 3. mean loss
    return top_loss[loss_mask].mean()


def focal_loss(y_pred, y_true, gamma: float = 2.0, normalize: bool = False):
    with torch.no_grad():
        p = y_pred.sigmoid()
        pt = (1 - p) * y_true + p * (1 - y_true)
        modulating_factor = pt.pow(gamma)

    if normalize:
        y_pred = y_pred.view(-1)
        y_true = y_true.float().view(-1)
        losses = F.binary_cross_entropy_with_logits(y_pred, y_true, reduction='none')

        modulated_losses = losses * modulating_factor
        scale = losses.sum() / modulated_losses.sum()
        return modulated_losses.sum() * scale
    else:
        return F.binary_cross_entropy_with_logits(y_pred, y_true, modulating_factor, reduction='mean')


@torch.jit.script
def sigmoid_focal_loss(y_pred, y_true, alpha: float = -1, gamma: float = 2, reduction: str = "mean"):
    # implementation of fvcore.nn.loss
    p = torch.sigmoid(y_pred)
    ce_loss = F.binary_cross_entropy_with_logits(
        y_pred, y_true, reduction="none"
    )
    p_t = p * y_true + (1 - p) * (1 - y_true)
    loss = ce_loss * ((1 - p_t) ** gamma)

    if alpha >= 0:
        alpha_t = alpha * y_true + (1 - alpha) * (1 - y_true)
        loss = alpha_t * loss

    if reduction == "mean":
        loss = loss.mean()
    elif reduction == "sum":
        loss = loss.sum()

    return loss


@torch.jit.script
def soft_cross_entropy(input: torch.Tensor, target: torch.Tensor):
    assert input.dim() == 4 and target.dim() == 4
    log_probs = F.log_softmax(input, dim=1)
    return -(target * log_probs).mean(dim=(0, 2, 3)).sum()


class InverseWeightCrossEntroyLoss(nn.Module):
    def __init__(self, class_num, ignore_index=255):
        super(InverseWeightCrossEntroyLoss, self).__init__()
        self.class_num = class_num
        self.ignore_index = ignore_index

    def forward(self, logit, label):
        """
       get inverse cross entropy loss
        Args:
            logit: a tensor, [batch_size, num_class, image_size, image_size]
            label: a tensor, [batch_size, image_size, image_size]
        Returns:
        """
        inverse_weight = self.get_inverse_weight(label)
        cross_entropy = nn.CrossEntropyLoss(weight=inverse_weight, ignore_index=self.ignore_index).cuda()
        inv_w_loss = cross_entropy(logit, label)
        return inv_w_loss

    def get_inverse_weight(self, label):
        mask = (label >= 0) & (label < self.class_num)
        label = label[mask]
        # reduce dim
        total_num = len(label)
        # get unique label, convert unique label to list
        percentage = torch.bincount(label, minlength=self.class_num) / float(total_num)
        # get inverse
        w_for_each_class = 1 / torch.log(1.02 + percentage)
        # convert to tensor
        return w_for_each_class.float()


class StructureLoss(nn.Module):
    """Ref SOD F3Net"""

    def __init__(self, kernel_size=31, stride=1, padding=15):
        super(StructureLoss, self).__init__()
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding

    def _get_weight(self, mask):
        weit = 1 + 5 * torch.abs(F.avg_pool2d(mask, kernel_size=self.kernel_size, stride=self.stride, padding=self.padding) - mask)
        return weit

    def forward(self, pred, mask):
        weit = self._get_weight(mask)

        wbce = F.binary_cross_entropy_with_logits(pred, mask, reduce='none')
        wbce = (weit * wbce).sum(dim=(2, 3)) / weit.sum(dim=(2, 3))

        pred = torch.sigmoid(pred)
        inter = ((pred * mask) * weit).sum(dim=(2, 3))
        union = ((pred + mask) * weit).sum(dim=(2, 3))
        wiou = 1 - (inter + 1) / (union - inter + 1)
        return (wbce + wiou).mean()


class IOULoss(torch.nn.Module):
    def __init__(self, size_average=True):
        super().__init__()
        self.size_average = size_average

    @staticmethod
    def _iou(pred, target, size_average=True):
        b = pred.shape[0]
        IoU = 0.0
        for i in range(0, b):
            # compute the IoU of the foreground
            Iand1 = torch.sum(target[i, :, :, :] * pred[i, :, :, :])
            Ior1 = torch.sum(target[i, :, :, :]) + torch.sum(pred[i, :, :, :]) - Iand1
            IoU1 = Iand1 / Ior1

            # IoU loss is (1-IoU1)
            IoU = IoU + (1 - IoU1)

        return IoU / b

    def forward(self, pred, target):
        return self.iou(pred, target, self.size_average)


class SSIMLoss(nn.Module):
    """# https://github.com/Po-Hsun-Su/pytorch-ssim/blob/master/pytorch_ssim/__init__.py"""
    def __init__(self, window_size=11, size_average=True):
        super().__init__()
        self.window_size = window_size
        self.size_average = size_average
        self.channel = 1
        self.window = self.create_window(window_size, self.channel)

    @staticmethod
    def gaussian(window_size, sigma):
        gauss = torch.Tensor([math.exp(-(x - window_size // 2) ** 2 / float(2 * sigma ** 2)) for x in range(window_size)])
        return gauss / gauss.sum()

    def create_window(self, window_size, channel):
        _1D_window = self.gaussian(window_size, 1.5).unsqueeze(1)
        _2D_window = _1D_window.mm(_1D_window.t()).float().unsqueeze(0).unsqueeze(0)
        window = Variable(_2D_window.expand(channel, 1, window_size, window_size).contiguous())
        return window
    
    @staticmethod
    def ssim(img1, img2, window, window_size, channel, size_average=True):
        mu1 = F.conv2d(img1, window, padding=window_size // 2, groups=channel)
        mu2 = F.conv2d(img2, window, padding=window_size // 2, groups=channel)

        mu1_sq = mu1.pow(2)
        mu2_sq = mu2.pow(2)
        mu1_mu2 = mu1 * mu2

        sigma1_sq = F.conv2d(img1 * img1, window, padding=window_size // 2, groups=channel) - mu1_sq
        sigma2_sq = F.conv2d(img2 * img2, window, padding=window_size // 2, groups=channel) - mu2_sq
        sigma12 = F.conv2d(img1 * img2, window, padding=window_size // 2, groups=channel) - mu1_mu2

        C1 = 0.01 ** 2
        C2 = 0.03 ** 2

        ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))

        if size_average:
            return ssim_map.mean()
        else:
            return ssim_map.mean(1).mean(1).mean(1)

    def forward(self, img1, img2):
        (_, channel, _, _) = img1.size()

        if channel == self.channel and self.window.data.type() == img1.data.type():
            window = self.window
        else:
            window = self.create_window(self.window_size, channel)

            if img1.is_cuda:
                window = window.cuda(img1.get_device())
            window = window.type_as(img1)

            self.window = window
            self.channel = channel

        return self.ssim(img1, img2, window, self.window_size, channel, self.size_average)


class BCE_SSIM_IoU_Loss(nn.Module):
    """Ref BASNet"""
    def __init__(self, window_size=11):
        super(BCE_SSIM_IoU_Loss, self).__init__()

        self.bce = nn.BCEWithLogitsLoss()
        self.ssim = SSIMLoss(window_size=window_size)
        self.iou = IOULoss()

    def forward(self, pred, target):
        bce_out = self.bce(pred, target)
        ssim_out = 1 - self.ssim(pred, target)
        iou_out = self.iou(pred, target)
        loss = bce_out + ssim_out + iou_out

        return loss
