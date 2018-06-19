# Recursively walk over a directory and get all colocalization results of the
# images under the input folder 
#
# Usage:
#     python colocalization.py INPUT_DIR
# Author: Xiaofei Zhang
# June 15 2018

from skimage.io import imsave
from skimage.filters import threshold_otsu
import numpy as np
import sys
import os
from PIL import Image

rootdir = sys.argv[1]
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith('.jpg') or file.endswith('.tif'):
            fname = os.path.join(subdir, file)   
            print('Processing ' + fname + '...')
            base_name = fname[:-4]
            img = np.array(Image.open(fname).convert('RGB'))
            blue = img[:,:,2]
            green = img[:,:,1]
            red = img[:,:,0]
            b_and_g = np.zeros(blue.shape)
            b_and_r = np.zeros(blue.shape)
            g_and_r = np.zeros(blue.shape)
            b_and_g_and_r = np.zeros(blue.shape)
        
            thresh_g = threshold_otsu(green)
            thresh_b = threshold_otsu(blue)
            thresh_r = threshold_otsu(red)
            b_and_g[(blue>thresh_b)& (green>thresh_g)] = (blue[(blue>thresh_b)& (green>thresh_g)] + green[(blue>thresh_b)& (green>thresh_g)]) / 2
            b_and_r[(blue>thresh_b)& (red>thresh_r)] = (blue[(blue>thresh_b)& (red>thresh_r)] + red[(blue>thresh_b)& (red>thresh_r)]) / 2
            g_and_r[(green>thresh_g)& (red>thresh_r)] = (green[(green>thresh_g)& (red>thresh_r)] + red[(green>thresh_g)& (red>thresh_r)]) / 2
            b_and_g_and_r[(blue>thresh_b) & (green>thresh_g)& (red>thresh_r)] = (blue[(blue>thresh_b) & (green>thresh_g)& (red>thresh_r)] + green[(blue>thresh_b) & (green>thresh_g)& (red>thresh_r)] + red[(blue>thresh_b) & (green>thresh_g)& (red>thresh_r)]) / 3

            if np.count_nonzero(b_and_g):
                imsave(base_name + '_blue_and_green.jpg',b_and_g.astype(int))
            if np.count_nonzero(b_and_r):
                imsave(base_name + '_blue_and_red.jpg',b_and_r.astype(int))
            if np.count_nonzero(g_and_r):
                imsave(base_name + '_green_and_red.jpg',g_and_r.astype(int))
            if np.count_nonzero(b_and_g_and_r):
                imsave(base_name + '_blue_and_green_and_red.jpg',b_and_g_and_r.astype(int))
