from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .line import LineDetector
from .line_detector import NewLineDetector

detector_factory = {
  'line': LineDetector, 
  'line_4_cat': NewLineDetector,
  'line_2_cat': NewLineDetector
}