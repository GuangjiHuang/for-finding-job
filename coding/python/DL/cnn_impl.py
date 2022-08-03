import numpy as np
import torch.nn.functional as F
import torch
import cv2

def conv2d(in_fm, weights, stride, padding):
    # the * is the convolution operator
    # in_fm * wights = out_fm
    """"""
    # step1: get the shape of the in_fm and the weights
    # step2: calculate the shape of the out_fm, and then create the matrix of the out_fm
    # step3: assign the value to the out_fm, make the loop of the conv computation
    """"""
    """
    :param in_fm: the input feeture map
    :param weights: the weight
    :param stride: the sride
    :param padding: the padding
    :return: the output feature map: out_mp
    """
    # step1 : get the parameter
    h_in, w_in, c_in = in_fm.shape
    k = weights.shape[0]
    s = stride
    p = padding
    # step 2: cal the out_mp's height, width and the channel(is the 1)
    h_out = (h_in + 2 * p - k) // s + 1
    w_out = (w_in + 2 * p - k) // s + 1
    out_fm = np.zeros((h_out, w_out))
    # add the padding
    in_fm_p = np.zeros((h_in+2*p, w_in+2*p, 3))
    in_fm_p[p:+h_in+p, p:+w_in+p] = in_fm
    # step 3:
    for r in range(h_out):
        for c in range(w_out):
            roi = in_fm_p[r*s:r*s+k, c*s:c*s+k, :]
            mul_mat = roi * weights
            out_fm[r][c] = np.sum(mul_mat)
    #
    return out_fm

if __name__ == "__main__":
    torch.random.manual_seed(0)
    i_img = torch.randint(0, 2, (1, 3, 10, 10))
    weight = torch.randint(0, 2, (1, 3, 5, 5))
    # cal the conv
    ret = F.conv2d(i_img, weight, padding=1, stride=2)
    ret = torch.squeeze(ret)
    print(ret.shape)
    print(ret)
    #
    print("my own conv")
    input_img_np = np.transpose(i_img.numpy().squeeze(), (1, 2, 0))
    weight_np = np.transpose(weight.numpy().squeeze(), (1, 2, 0))
    ret_conv = conv2d(input_img_np, weight_np, 2, 1)
    print(ret_conv.shape)
    print(ret_conv)





















