# -*- encoding: utf-8 -*-
"""
Copyright (c) Yuwei Jin
Created on 2021/5/14 上午8:53
Written by Yuwei Jin (yuwei_jin@163.com)
"""

import os
import cv2
import math
import json

import numpy as np
from PIL import Image
from multiprocessing import Pool

from sv.libs.tools import utils


class DilatedCrop:
    """Crop a big image and corresponding label into small patches
        mainly used for inferring.
    """

    def __init__(self, crop_cfg, use_pil_read=False):
        self.patch_size = crop_cfg['patch_size']
        self.win = crop_cfg['win_size']
        self.im_suffix = crop_cfg['im_suffix']
        self.gt_suffix = crop_cfg['gt_suffix']
        self.dataset_cfg = crop_cfg['dataset_cfg']

        self.dataset_name = crop_cfg['dataset_name']
        root_dir = crop_cfg['root_dir']

        output_root_dir = crop_cfg['output_root_dir']
        output_root_dir = os.path.join(output_root_dir, 'test')

        self.im_src = os.path.join(root_dir, 'image')
        self.gt_src = os.path.join(root_dir, 'label')

        self.im_output_src = os.path.join(output_root_dir, 'image')
        self.gt_output_src = os.path.join(output_root_dir, 'label')
        self.crop_info_dir = os.path.join(output_root_dir, 'crop_info')

        self.use_pil_read = use_pil_read


    def save_crop_info(self, im, im_name):
        rows, cols = im.shape[0], im.shape[1]
        m = math.ceil(rows / self.win)
        n = math.ceil(cols / self.win)

        info = {'rows': rows,
                'cols': cols,
                'patch_size': self.patch_size,
                'central_win_size': self.win,
                'm': m,
                'n': n
                }

        with open(os.path.join(self.crop_info_dir, im_name + '_crop_info.json'), 'w') as f:
            f.write(json.dumps(info))

    def _crop(self, im_name):
        """im_name example: test1.tif"""
        # applying PIL to load big scale images
        if self.use_pil_read:
            Image.MAX_IMAGE_PIXELS = None
            im = Image.open(os.path.join(self.im_src, im_name)).convert('RGB')
            gt = Image.open(os.path.join(self.gt_src, im_name)).convert('L')
            im = np.array(im)
            gt = np.array(gt)
        else:
            im = cv2.imread(os.path.join(self.im_src, im_name))
            gt = cv2.imread(os.path.join(self.gt_src, im_name), cv2.IMREAD_GRAYSCALE)

        print('processing: ' + im_name)
        im_name, _ = im_name.split('.')
        self.save_crop_info(im, im_name)

        # pad image and label
        rows, cols = im.shape[0], im.shape[1]
        win = self.win
        patch_size = self.patch_size
        m = math.ceil(rows / win)
        n = math.ceil(cols / win)
        pad = (patch_size - win) // 2

        top = pad
        bottom = win * m - rows + pad
        left = pad
        right = win * n - cols + pad

        mean, std = utils.load_mean_std(self.dataset_cfg)
        im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=mean)
        gt = cv2.copyMakeBorder(gt, top, bottom, left, right, cv2.BORDER_CONSTANT, value=0)

        if self.use_pil_read:
            im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)

        k = 0
        for i in range(m):
            x1 = i * win + top - pad
            x2 = x1 + win + 2 * pad
            if i == 0:
                x1, x2 = 0, patch_size

            for j in range(n):
                y1 = j * win - pad + left
                y2 = y1 + win + 2 * pad
                if j == 0:
                    y1, y2 = 0, patch_size

                im_patch = im[x1:x2, y1:y2, :]
                gt_patch = gt[x1:x2, y1:y2]

                k += 1
                im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
                cv2.imwrite(os.path.join(self.im_output_src, im_name + '-' + str(k) + self.im_suffix), im_patch)
                cv2.imwrite(os.path.join(self.gt_output_src, im_name + '-' + str(k) + self.im_suffix), gt_patch)

    @utils.time_counter
    def crop(self):
        utils.mk_dirs_r(self.im_output_src)
        utils.mk_dirs_r(self.gt_output_src)
        utils.mk_dirs_r(self.crop_info_dir)

        im_lists = utils.get_im_name_list(self.im_src, self.im_suffix)
        if len(im_lists) >= 8:  # applying multi processing
            pool = Pool(processes=16)
            pool.map(self._crop, im_lists)
            pool.close()
            pool.join()
        else:
            for f in im_lists:
                self._crop(f)
