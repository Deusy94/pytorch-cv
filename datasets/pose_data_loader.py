#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Donny You(youansheng@gmail.com)
# Class for the Pose Data Loader.


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from torch.utils import data

import datasets.tools.transforms as trans
from utils.logger import Logger as Log


class PoseDataLoader(object):

    def __init__(self, configer):
        self.configer = configer

        self.base_train_transform = trans.BaseCompose([
            trans.RandomResize(),
            trans.RandomRotate(self.configer.get('data', 'rotate_degree')),
            trans.RandomCrop(self.configer.get('data', 'input_size')),
            trans.RandomResize(size=self.configer.get('data', 'input_size')), ])

        self.base_val_transform = trans.BaseCompose([
            trans.RandomCrop(self.configer.get('data', 'input_size')),
            trans.RandomResize(size=self.configer.get('data', 'input_size')), ])

        self.input_transform = trans.Compose([
            trans.ToTensor(),
            trans.Normalize(mean=[128.0, 128.0, 128.0],
                            std=[256.0, 256.0, 256.0]), ])

        self.label_transform = trans.Compose([trans.ToTensor(), ])

    def get_trainloader(self, Loader=None):
        if self.configer.get('dataset') == 'coco':
            coco_trainloader = data.DataLoader(
                Loader(root_dir=self.configer.get('data', 'train_dir'),
                       base_transform=self.base_train_transform,
                       input_transform=self.input_transform,
                       label_transform=self.label_transform,
                       split='train', configer=self.configer),
                batch_size=self.configer.get('data', 'batch_size'), shuffle=True,
                num_workers=self.configer.get('solver', 'workers'), pin_memory=True)

            return coco_trainloader

        elif self.configer.get('dataset') == 'lane':
            lane_trainloader = data.DataLoader(
                Loader(self.configer.get('data', 'train_dir'),
                       base_transform=self.base_train_transform,
                       input_transform=self.input_transform,
                       label_transform=self.label_transform,
                       split='train', configer=self.configer),
                batch_size=self.configer.get('data', 'batch_size'), shuffle=True,
                num_workers=self.configer.get('solver', 'workers'), pin_memory=True)

            return lane_trainloader

        else:
            Log.error('Dataset: {} is invalid.'.format(self.configer.get('dataset')))
            return None

    def get_valloader(self, Loader=None):
        if self.configer.get('dataset') == 'coco':
            coco_valloader = data.DataLoader(
                Loader(root_dir=self.configer.get('data', 'val_dir'),
                       base_transform=self.base_val_transform,
                       input_transform=self.input_transform,
                       label_transform=self.label_transform,
                       split='val', configer=self.configer),
                batch_size=self.configer.get('data', 'batch_size'), shuffle=False,
                num_workers=self.configer.get('solver', 'workers'), pin_memory=True)

            return coco_valloader

        elif self.configer.get('dataset') == 'lane':
            lane_valloader = data.DataLoader(
                Loader(self.configer.get('data', 'val_dir'),
                       base_transform=self.base_val_transform,
                       input_transform=self.input_transform,
                       label_transform=self.label_transform,
                       split='val', configer=self.configer),
                batch_size=self.configer.get('data', 'batch_size'), shuffle=False,
                num_workers=self.configer.get('solver', 'workers'), pin_memory=True)

            return lane_valloader

        else:
            Log.error('Dataset: {} is invalid.'.format(self.configer.get('dataset')))
            return None

if __name__ == "__main__":
    # Test data loader.
    pass