from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import _init_paths

import os
import cv2

from opts import opts
from detectors.detector_factory import detector_factory

def demo(opt):

  Detector = detector_factory[opt.dataset]
  detector = Detector(opt)
  
  if os.path.isdir(opt.demo):
    image_names = []
    ls = os.listdir(opt.demo)
    for file_name in sorted(ls):
      image_names.append(os.path.join(opt.demo, file_name))
  else:
    image_names = [opt.demo]
  
  for image in image_names:
    ret = detector.run(image)

if __name__ == '__main__':
  opt = opts().init()
  demo(opt)
