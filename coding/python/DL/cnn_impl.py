import numpy as np
import cv2

def conv2d(input_img, c_out, k, s, p):
    # get the input feature map's height, width, channels
    h_in, w_in, c_in = input_img.shape
    # get the output feature map's height, width, channels
    weight = np.random.rand((k, k, ))
    h_out = (h_in + 2*p - k) // s + 1
    w_out = (w_in + 2*p - k) // s + 1
    output_img = np.zeros((h_out, w_out, c_out))
    # init the weight
    weight = np.random.randn((c_out, k, k, c_in))
    # create the output image
    # then calculate the conv
    # output_img = input_img * wight
    # make the loop for the channels, the height, then the width
    for c in range(c_out):
        for w in range(w_out):
            for h in range(h_out):
                # we can get the
                output_img[h][w][c] = temp
    # there will be many of the loop ? what should I do for it ?




