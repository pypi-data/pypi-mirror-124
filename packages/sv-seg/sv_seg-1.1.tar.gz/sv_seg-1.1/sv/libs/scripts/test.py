# -*- coding: UTF-8 -*-
"""
Copyright (c) Yuwei Jin
Created at 2021-05-13 14:10
Written by Yuwei Jin (642281525@qq.com)
"""

import torch
import warnings
from tqdm import tqdm

from sv.libs.core.infer import Infer
from sv.libs.data.dataset.dataset import load_test_data
from sv.libs.tools import utils

warnings.filterwarnings("ignore")

# load well-trained model weights from disk.


class Test(Infer):
    def __init__(self, model, metrics, cfg):
        super(Test, self).__init__(model, cfg)

        self.evaluator = metrics

        self.test_data = load_test_data(cfg)
        self.cfg = cfg

    def test(self):
        with torch.no_grad():
            for i, (im_name, im, gt) in enumerate(tqdm(self.test_data, ncols=80, desc='inferring')):
                prob = self.forward(im)

                im_name, _ = im_name[-1].split('.')
                if isinstance(prob, (list, tuple)):
                    prob = prob[0]

                self.evaluator.cal_batch_metric(im_name, prob, gt)

                if self.cfg.TEST.SAVE_RES:
                    utils.save_prob_map(im_name, prob, self.cfg)
                    if not self.cfg.TEST.STITCH_RES:
                        utils.save_alpha_map(im_name, prob, gt, self.cfg)

        self.evaluator.average()


# def test():
#     # if cfg.TEST.SAVE_RES:
#     #     utils.mk_dirs_r(cfg.TEST.PROB_SAVE_DIR)
#     #
#     # Test()()
#     if cfg.TEST.STITCH_RES:
#         from tools.stitch_probs import Stitch
#         Stitch()()

#
# if __name__ == '__main__':
#     test()
