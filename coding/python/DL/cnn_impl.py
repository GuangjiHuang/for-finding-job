import numpy as np
import torch.nn.functional as F
import torch
import cv2

def conv2d(in_fm, weights, stride, padding):
    """
    :param in_fm: the input feeture map
    :param weights: the weight
    :param stride: the sride
    :param padding: the padding
    :return: the output feature map: out_mp
    """
    # get the parameter
    h_in, w_in, c_in = in_fm.shape
    k = weights.shape[0]
    s = stride
    p = padding
    # cal the out_mp's height, width and the channel(is the 1)
    h_out = (h_in + 2 * p - k) // s
    w_out = (w_in + 2 * p - k) // s
    out_fm = np.zeros((h_out, w_out), np.float32)
    #
    for i in range












# the main function
if __name__ == "__main__":
    np.random.seed(0)
    input_img = np.random.rand(1, 3, 10, 10)
    weight = np.random.rand(1, 3, 3, 3)
    # cal the conv
    input_img = torch.tensor(input_img)
    weight = torch.tensor(weight)
    print(input_img)
    print(weight)
    ret = F.conv2d(input_img, weight, padding=1)


