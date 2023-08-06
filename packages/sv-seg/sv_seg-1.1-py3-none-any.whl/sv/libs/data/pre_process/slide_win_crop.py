# -*- coding: UTF-8 -*-
"""
Copyright (c) Yuwei Jin
Created at 2021-10-23 21:43 
Written by Yuwei Jin (642281525@qq.com)
"""

import os
import cv2
import math
import json

import numpy as np
from PIL import Image
from multiprocessing import Pool

from sv.libs.tools import utils


class SlideWinCrop:
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
        self.phase = crop_cfg['phase']

        root_dir = crop_cfg['root_dir']

        output_root_dir = crop_cfg['output_root_dir']
        output_root_dir = os.path.join(output_root_dir, 'test')

        self.im_src = os.path.join(root_dir, 'image')
        self.gt_src = os.path.join(root_dir, 'label')

        self.im_output_src = os.path.join(output_root_dir, 'image')
        self.gt_output_src = os.path.join(output_root_dir, 'label')
        self.crop_info_dir = os.path.join(output_root_dir, 'crop_info')

        self.use_pil_read = use_pil_read
