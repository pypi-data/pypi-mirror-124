# -*- coding: UTF-8 -*-
"""
Copyright (c) Yuwei Jin
Created at 2021-10-23 20:23 
Written by Yuwei Jin (642281525@qq.com)
"""
import math
import os
import random
import re
import shutil
import time

import cv2
import numpy as np
import pandas as pd
from PIL import Image
from torch import Tensor

from torch.nn import functional as F

# ---------------- file IO related utils ---------------------
import torch

from sv.libs.core.lr_scheduler import PolyLR, ExponentialLR, PolyLR, CosineLR, StepLR


def mk_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def mk_dirs_r(file_path):
    if os.path.exists(file_path):
        shutil.rmtree(file_path, ignore_errors=True)
    os.makedirs(file_path, exist_ok=True)


def rm_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def get_im_name_list(path, im_extensions='.tif'):
    """return example:
        ['1.tif', '2.tif']
    """
    out = []
    for f in os.listdir(path):
        if f.endswith(im_extensions):
            out.append(f)
    return out


def load_mean_std(cfg):
    """ loading mean and std config"""
    d = cfg.DATASET
    # load mean std
    if d.MEAN_STD == 'imagenet':
        mean = [0.485, 0.456, 0.406]  # imagenet mean and std value
        std = [0.229, 0.224, 0.225]
        return mean, std
    else:
        mean_std_file = os.path.join(d.TRAIN_SET, os.path.join(d.TRAIN_SET, d.NAME + '_mean_std.csv'))
        try:
            data = pd.read_csv(mean_std_file)
            mean = data['mean'].values.tolist()
            std = data['std'].values.tolist()
            return mean, std
        except FileNotFoundError:
            print('{} mean-std.csv file is not found.'.format(mean_std_file))


def save_train_cfg(cfg):
    import json
    save_dir = cfg.MODEL.OUTPUT_DIR
    mk_dirs_r(save_dir)
    file_name = "training_cfg.json"
    save_dir = os.path.join(save_dir, file_name)
    with open(save_dir, 'w+', encoding='utf-8') as f:
        json.dump(cfg, f, ensure_ascii=False)


def list_to_txt(str_list, output_name):
    with open(output_name, 'w') as f:
        for s in str_list:
            f.write(str(s) + '\n')


def txt_to_list(txt_file) -> list:
    out = []
    with open(txt_file, 'r') as f:
        lines = f.readlines()
        for s in lines:
            out.append(s.rstrip("\n"))
    return out


# ---------------- time consumption related utils ---------------------
class TimeCounter:
    def __init__(self, return_sec=False):
        self.start_time = 0
        self.end_time = 0

        self.return_sec = return_sec

    def tic(self):
        self.start_time = time.time()

    def toc(self):
        """default return seconds"""
        end_time = time.time()
        t = end_time - self.start_time
        t = round(t, 2)

        if self.return_sec:
            return t
        else:
            return t / 60


def time_counter(func):
    def inner(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        return (end - start) / 60.

    return inner


# ---------------- training, validate, and test related utils ---------------------
def fast_hist(input: np.ndarray, label: np.ndarray, num_class: int) -> np.ndarray:
    """calculation confusion matrix"""
    assert input.shape == label.shape

    input = input.flatten().astype('int')
    label = label.flatten().astype('int')

    mask = (label >= 0) & (label < num_class)  # 去除边界为0的情况
    label = num_class * label[mask] + input[mask]
    count = np.bincount(label, minlength=num_class ** 2)
    conf_mat = count.reshape(num_class, num_class)

    return conf_mat


# ---------------- tensor related utils ---------------------
def is_tensor(img):
    return isinstance(img, torch.Tensor)


def is_numpy_array(img):
    return isinstance(img, np.ndarray)


def tensor_to_numpy(data: torch.Tensor) -> np.ndarray:
    """Convert tensor data to numpy"""
    if is_tensor(data):
        data = data.squeeze().detach().cpu().numpy()
        return data
    else:
        raise TypeError('input data should be Tensor type. Got {}'.format(type(data)))


def tensor_binarize(prob: torch.Tensor, cfg) -> np.ndarray:
    if cfg.MODEL.OUTPUT_CHANNELS > 1:
        prob = torch.softmax(prob, dim=1)
        pred = torch.argmax(prob, dim=1)
    else:
        prob = torch.sigmoid(prob)
        pred = prob > 0.5

    pred = tensor_to_numpy(pred)

    return pred


# ---------------- training and validate utils ---------------------
def fixed_np_random_seed(seed=2048):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)


def fixed_torch_seed(cfg):
    seed = cfg.TRAIN.SEED
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    # torch.cuda.manual_seed_all(seed) # if you are using multi-GPU.
    if cfg.TRAIN.CUDNN_DETERMINISTIC:
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def parse_lr_scheduler(cfg, optimizer, train_data):
    train_batch_steps = math.floor(len(train_data.dataset) / cfg.TRAIN.BATCH_SIZE)

    lr = cfg.TRAIN.LR
    warm_epoch = lr.WARMUP_EPOCH
    warm_start_lr = lr.WARMUP_START_LR

    if re.search(lr.SCHEDULER, 'ExponentialLR', re.IGNORECASE):
        scheduler = ExponentialLR(optimizer=optimizer, gamma=lr.POWER, eta_min_lr=lr.ETA_MIN_LR, warm_start_lr=warm_start_lr,
                                  warm_period=warm_epoch)
    elif re.search(lr.SCHEDULER, 'Poly', re.IGNORECASE):
        max_iters = cfg.TRAIN.EPOCHS * train_batch_steps
        warmup_period = warm_epoch * train_batch_steps
        scheduler = PolyLR(optimizer=optimizer, power=lr.POWER, max_iterations=max_iters, warm_start_lr=warm_start_lr,
                           warm_period=warmup_period)

    elif re.search(lr.SCHEDULER, 'Cosine', re.IGNORECASE):
        max_iters = cfg.TRAIN.EPOCHS * train_batch_steps
        warmup_period = lr.WARMUP_STEPS * train_batch_steps
        scheduler = CosineLR(optimizer=optimizer, eta_min_lr=lr.ETA_MIN_LR, T_max=max_iters, warm_start_lr=warm_start_lr,
                             warm_period=warmup_period)
    elif re.search(lr.SCHEDULER, 'Step', re.IGNORECASE):
        scheduler = StepLR(optimizer=optimizer, warm_start_lr=warm_start_lr, step_size=lr.STEP_SIZE, warm_period=warm_epoch,
                           gamma=lr.POWER)
    else:
        raise NotImplementedError("{} is not implemented.".format(lr.SCHEDULER))

    return scheduler


# ---------------- saving utils ---------------------
def save_binary_map(prob: torch.Tensor, im_name: str, save_dir: str, cfg):
    res = tensor_binarize(prob) * 255  # res
    filename = os.path.join(save_dir, cfg.MODEL.NAME + '_' + im_name + '_binary.png')
    cv2.imwrite(filename, res)


def save_prob_map(im_name, prob, cfg, save_dir=None):
    if is_tensor(prob):
        if cfg.MODEL.OUTPUT_CHANNELS > 1:
            prob = torch.softmax(prob, dim=1)
            prob = tensor_to_numpy(prob)[1, :, :]
        else:
            prob = torch.sigmoid(prob)
            # prob = torch.relu(prob)
            prob = tensor_to_numpy(data=prob)
            # eps = 1e-10
            # prob = prob / (prob.max() + eps)
            # prob = np.where(prob<0, 0, prob)

    prob = np.round(prob * 255)

    save_dir = cfg.TEST.PROB_SAVE_DIR if save_dir is None else save_dir
    filename = os.path.join(save_dir, cfg.MODEL.NAME + '_' + im_name + '_prob.png')
    cv2.imwrite(filename, prob.astype(np.uint8))


def save_palette_map(im_name, prob, gt, cfg):
    # obtain binary prediction
    if isinstance(prob, np.ndarray):
        p = prob > 0.5
    else:
        p = tensor_binarize(prob)

    def inner_fun(p_flg, gt_flag, color):
        r = np.where((p == p_flg) & (gt == gt_flag), color[0], 0)
        g = np.where((p == p_flg) & (gt == gt_flag), color[1], 0)
        b = np.where((p == p_flg) & (gt == gt_flag), color[2], 0)
        return cv2.merge([b, g, r]).astype(np.uint8)

    bg = inner_fun(0, 0, cfg.TEST.BACKGROUND_COLOR)
    tp = inner_fun(1, 1, cfg.TEST.TP_COLOR)
    fp = inner_fun(1, 0, cfg.TEST.FP_COLOR)
    fn = inner_fun(0, 1, cfg.TEST.FN_COLOR)

    out = (tp + bg + fp + fn)

    save_dir = cfg.TEST.PROB_SAVE_DIR
    output_path = os.path.join(save_dir, cfg.MODEL.NAME + '_' + im_name + '_palette.png')
    cv2.imwrite(output_path, out)


def save_alpha_map(im_name, prob, gt, cfg, save_dir=None):
    data = cfg.DATASET
    save_dir = cfg.TEST.PROB_SAVE_DIR
    if cfg.TEST.STITCH_RES:
        ori_image = Image.open(os.path.join(data.TEST_WHOLE_IMAGE, im_name + data.IMG_EXTENSION)).convert('RGBA')
    else:
        ori_image = Image.open(os.path.join(data.TEST_SET, 'image', im_name + data.IMG_EXTENSION)).convert('RGBA')

    if not is_tensor(prob):
        p = prob > 0.5
    else:
        p = tensor_binarize(prob)

    def inner_fun(p_flg, gt_flag, color):
        r = np.where((p == p_flg) & (gt == gt_flag), color[0], 0)
        g = np.where((p == p_flg) & (gt == gt_flag), color[1], 0)
        b = np.where((p == p_flg) & (gt == gt_flag), color[2], 0)
        return cv2.merge([r, g, b]).astype(np.uint8)

    tp = inner_fun(1, 1, cfg.TEST.TP_COLOR)
    fp = inner_fun(1, 0, cfg.TEST.FP_COLOR)
    fn = inner_fun(0, 1, cfg.TEST.FN_COLOR)

    mask = (tp + fp + fn)
    mask = Image.fromarray(mask).convert('RGBA')
    image = Image.blend(ori_image, mask, cfg.TEST.ALPHA)

    # image_rgba = np.array(image)
    # ori_image = np.array(ori_image)
    # #
    # ori_image[:, :, 0] = np.where(p[:, :] == 1, image_rgba[:, :, 0], ori_image[:, :, 0])
    # ori_image[:, :, 1] = np.where(p[:, :] == 1, image_rgba[:, :, 1], ori_image[:, :, 1])
    # ori_image[:, :, 2] = np.where(p[:, :] == 1, image_rgba[:, :, 2], ori_image[:, :, 2])
    # #
    # image = Image.fromarray(ori_image.astype(np.uint8))

    save_dir = cfg.TEST.PROB_SAVE_DIR if save_dir is None else save_dir
    image.save(os.path.join(save_dir, cfg.MODEL.NAME + '_' + im_name + '_alpha.png'))


def edge_extraction(x: torch.Tensor, operator='laplacian') -> torch.Tensor:
    """extract the edge of feature map by utilizing specific kernel operator
    Args:
        x: input feature map (type: torch.Tensor)
        operator: 'laplacian', 'sobel', 'prewitt', default is laplacian
    Return:
        soft edge
    """

    def _conv2d(input, kernel):
        kernel.requires_grad = False
        return F.conv2d(input, weight=kernel, padding=1, stride=1, bias=None)

    if operator == 'laplacian':
        kernel = -1 * torch.ones(1, 1, 3, 3)
        kernel[:, :, 1, 1] = 8.
        return _conv2d(x, kernel)
    elif operator == 'sobel':
        kernel_x = torch.Tensor([[[[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]]])
        gx = _conv2d(input, kernel_x)
        kernel_y = torch.Tensor([[[[1, 2, 1], [0, 0, 0], [-1, -2, -1]]]])
        gy = _conv2d(input, kernel_y)
        return torch.sqrt(torch.pow(gx, 2) + torch.pow(gy, 2))
    elif operator == 'prewitt':
        kernel_x = torch.Tensor([[[[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]]])
        gx = _conv2d(input, kernel_x)
        kernel_y = torch.Tensor([[[[1, 1, 1], [0, 0, 0], [-1, -1, -1]]]])
        gy = _conv2d(input, kernel_y)
        return torch.sqrt(torch.pow(gx, 2) + torch.pow(gy, 2))
    else:
        raise NotImplementedError


def channel_shuffle(x, groups):
    batch_size, num_channels, height, width = x.data.size()

    channels_per_group = num_channels // groups

    # reshape
    x = x.view(batch_size, groups, channels_per_group, height, width)

    # transpose
    # - contiguous() required if transpose() is used before view().
    #   See https://github.com/pytorch/pytorch/issues/764
    x = torch.transpose(x, 1, 2).contiguous()

    # flatten
    x = x.view(batch_size, -1, height, width)

    return x


def global_weighted_average_pool(x):
    eps = 1e-10
    b, c, _, _ = x.size()
    x1 = x.view(b, c, -1)
    w = x / (torch.sum(x1, dim=2).view(b, c, 1, 1) + eps)
    y = x * w
    y = y.view(b, c, -1)
    y = torch.sum(y, dim=2).view(b, c, 1, 1)


def cal_fps(model, input_size=(3, 512, 512), epochs=200):
    tic = torch.cuda.Event(enable_timing=True)
    toc = torch.cuda.Event(enable_timing=True)

    times = np.zeros((epochs, 1))

    model = model.cuda().eval()
    x = torch.randn(input_size).unsqueeze(dim=0).cuda()

    # GPU-WARM-UP
    with torch.no_grad():
        for _ in range(20):
            _ = model(x)

    # MEASURE PERFORMANCE
    mean_time, fps = [], []
    for _ in range(3):
        with torch.no_grad():
            for epoch in range(epochs):
                tic.record()
                _ = model(x)
                toc.record()
                # WAIT FOR GPU SYNC
                torch.cuda.synchronize()
                times[epoch] = tic.elapsed_time(toc)

        temp = np.sum(times) / epochs
        mean_time.append(temp)
        fps.append(1000.0 / temp)
    print('mean: {:.3f}ms, fps: {:.2f}'.format(np.mean(mean_time), np.mean(fps)))


def get_distance_transform(label: np.ndarray) -> Tensor:
    """binary label distance transform"""
    label = np.uint8(label)
    dist = cv2.distanceTransform(label, cv2.DIST_L2, 0)
    eps = 1e-10
    dist = dist / (dist.max() + eps)

    dist = np.where((0.3 > dist) & (dist > 0), 1, 0)

    # plt.imshow(dist)
    # plt.show()

    # convert to tensor
    dist = torch.from_numpy(dist).unsqueeze(dim=0).cuda()

    return dist


def add_list_to_dataframe(data, index, df):
    """Convert list to DataFrame"""
    columns = df.columns
    dic = dict(map(lambda x, y: [x, y], columns, data))
    df.loc[index] = dic

    return df
