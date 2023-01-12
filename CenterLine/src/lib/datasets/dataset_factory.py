from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .sample.line import LineDataset

from .dataset.roboline import ROBOLINE
from .dataset.random_synthetic import RANDOM_SYNTHETIC
from .dataset.random_4_categories  import RANDOM_4CAT
from .dataset.random_2_categories  import RANDOM_2CAT


dataset_factory = {
  'roboline': ROBOLINE ,
  'random_synthetic': RANDOM_SYNTHETIC,
  "line_4_cat": RANDOM_4CAT,
  "line_2_cat": RANDOM_2CAT
}

_sample_factory = {
  'line': LineDataset
}


def get_dataset(dataset, task):
  class Dataset(dataset_factory[dataset], _sample_factory[task]):
    pass
  return Dataset
  
