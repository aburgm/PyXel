# File: checks.py
# Author: Georgiana Ogrean
# Created on 06.05.2015
#
# Sanity checks to avoid running with incorrect input.
#
# Change log:

import pyfits
import numpy as np
from SurfMessages import *

def get_size(img):
  return np.size(img[0].data)

# Check that counts, exposure, and background maps have the same size
def check_map_size(img,expmap,bkgmap):
  if expmap is not None:
    if get_size(img) != get_size(expmap):
      raise SizeError('Count map and exposure map should have the same size.')
  if bkgmap is not None:
    if get_size(img) != get_size(bkgmap):
      raise SizeError('Count map and background map should have the same size.')

# Check that the region in which the profile is 
# created is a valid region. 
def check_shape(shape):
  if shape.lower() not in ('circle', 'panda', 'ellpanda'):
    raise ShapeError("Invalid region. Valid region are 'circle', 'panda', and 'ellpanda'.")

def check_params(shape, params):
  if shape.lower() == 'circle':
    if params[0] < 0. or params[0] > 360.
  elif shape.lower() == 'panda':
  elif shape.lower() == 'ellpanda':


