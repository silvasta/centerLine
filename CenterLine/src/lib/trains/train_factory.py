from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .line import LineTrainer
from .line_chamfer import LineTrainer as LineChamferTrainer

train_factory = {
  'line': LineTrainer,
  #'line_chamfer': LineChamferTrainer
}
