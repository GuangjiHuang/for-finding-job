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


def conv_v2(in_fm, weights, s, p):
    # get the in_fm  and the weights shape
    h_in, w_in, c_in = in_fm.shape
    k = weights.shape[0]
    # calculate the fm_out's shape
    h_out = (h_in + 2 * p - k) // s + 1
    w_out = (w_in + 2 * p - k) // s + 1
    # create the out_fm
    out_fm = np.zeros((h_out, w_out))
    # create the padding input feature map
    in_fm_p = np.zeros((h_in+2*p, w_in+2*p, c_in))
    in_fm_p[p:h_in+p, p:w_in+p] = in_fm
    # then conv and loop
    for h in range(h_out):
        for w in range(w_out):
            out_fm[h][w] = np.sum(weights * in_fm_p[h*s:h*s+k, w*s:w*s+k])
    # and then return the result
    return out_fm

def conv_v3(in_fm, weights, s, p):
    # get the shape of the in_fm and the weights
    h_in, w_in, c_in = in_fm.shape
    k = weights.shape[0]
    # calculate the h_out and the w_out
    h_out = (h_in + 2 * p - k) // s + 1
    w_out = (w_in + 2 * p - k) // s + 1
    # create the out_Fm
    out_fm = np.zeros((h_out, w_out))
    # padding and then calculate the wise value
    in_fm_padding = np.zeros((h_in+2*p, w_in+2*p, c_in))
    in_fm_padding[p:p+h_in, p:p+w_in] = in_fm
    #
    for h in range(h_out):
        for w in range(w_out):
            out_fm[h][w] = np.sum(weights * in_fm_padding[s*h:s*h+k, s*w:s*w+k])
    return out_fm
# the conv 4 time: 2022-8-15
def conv_v4(in_fm, weights, s, p):
    # get the shap of the in_fm and the weights
    h_in, w_in, c_in = in_fm.shape
    k = weights.shape[0]
    # calculate the out_fm's shape
    h_out = (h_in + 2*p - k) // s + 1
    w_out = (w_in + 2*p - k) // s + 1
    # create the out_fm
    out_fm = np.zeros((h_out, w_out))
    # padding and then calculate the output
    in_fm_padding = np.zeros((h_in+2*p, w_in+2*p, c_in))
    in_fm_padding[p:h_in+p, p:w_in+p] = in_fm
    #
    for h in range(h_out):
        for w in range(w_out):
            out_fm[h][w] = np.sum(weights*in_fm_padding[s*h:s*h+k, s*w:s*w+k])
    #
    return out_fm

if __name__ == "__main__":
    torch.random.manual_seed(0)
    i_img = torch.randint(0, 2, (1, 3, 10, 10))
    weight = torch.randint(0, 2, (1, 3, 3, 3))
    p = 1
    s = 2
    # cal the conv
    ret = F.conv2d(i_img, weight, stride=s, padding=p)
    ret = torch.squeeze(ret)
    print(ret.shape)
    print(ret)
    #
    print("my own conv")
    input_img_np = np.transpose(i_img.numpy().squeeze(), (1, 2, 0))
    weight_np = np.transpose(weight.numpy().squeeze(), (1, 2, 0))
    ret_conv = conv2d(input_img_np, weight_np, s, p)
    print(ret_conv.shape)
    print(ret_conv)
    #
    print("my second conv")
    ret_conv_3th = conv_v3(input_img_np, weight_np, s, p)
    print(ret_conv_3th)
    #
    print("my forth conv")
    ret_conv_4th = conv_v4(input_img_np, weight_np, s, p)
    print(ret_conv_4th)






















