from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import _init_paths

import os
# import json
# import cv2
# import numpy as np
# import time
from progress.bar import Bar
import torch
from pycocotools.cocoeval import COCOeval

# from external.nms import soft_nms
from opts import opts
from logger import Logger
from utils.metric import run_metric
from datasets.dataset_factory import dataset_factory
from detectors.detector_factory import detector_factory

def test(opt):
  os.environ['CUDA_VISIBLE_DEVICES'] = opt.gpus_str

  Dataset = dataset_factory[opt.dataset]
  opt = opts().update_dataset_info_and_set_heads(opt, Dataset)
  Logger(opt)
  Detector = detector_factory[opt.dataset]
  print("Detector", Detector)
  dataset = Dataset(opt, "val")
  detector = Detector(opt)

  results = {}
  num_iters = len(dataset)

  for ind in range(num_iters):
    img_id = dataset.images[ind]
    img_info = dataset.coco.loadImgs(ids=[img_id])[0]
    img_path = os.path.join(dataset.img_dir, img_info['file_name'])

    ret = detector.run(img_path)
    
    results[img_id] = ret

  dataset.run_eval(results, opt.save_dir)
  run_metric(dataset.convert_eval_format(results), dataset.annot_path)




if __name__ == '__main__':
  opt = opts().parse()
  test(opt)