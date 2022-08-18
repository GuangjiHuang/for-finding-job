import numpy as np
import math
import cv2

def linearInter(src, dst_w, dst_h):
    # get the src shape and the scale
    o_h, o_w, c = src.shape
    scale_h, scale_w = o_h/dst_h, o_w/dst_w
    # create the dst_img
    dst_img = np.zeros((dst_h, dst_w, c))
    # cal the dst_img[h][w][c]
    for ch in range(c):
        for h in range(dst_h):
            for w in range(dst_w):
                # map the h, w, c -> src: h_, w_, c_
                h_ = h * (o_h-1) / (dst_h-1)
                w_ = w * (o_w-1) / (dst_w-1)
                # get the four nearest point
                x_0 = math.floor(w_)
                x_1 = math.ceil(w_)
                y_0 = math.floor(h_)
                y_1 = math.ceil(h_)
                # calculate the val_x_up, val_x_down, val_y
                val_lt = src[x_0][y_0][ch]
                val_rt = src[x_1][y_0][ch]
                val_lb = src[x_0][y_1][ch]
                val_rb = src[x_1][y_1][ch]
                if x_1 == x_0:
                    val_x_up = val_lt
                    val_x_down = val_lb
                else:
                    val_x_up = val_lt + (w_ - x_0) * (val_rt - val_lt) / (x_1 - x_0)
                    val_x_down = val_lb + (w_ - x_0) * (val_rb - val_lb) / (x_1 - x_0)
                if y_0 == y_1:
                    val_y = val_x_down
                else:
                    val_y = val_x_up + (h_ - y_0) * (val_x_down - val_x_up) / (y_1 - y_0)
                # assign the value
                dst_img[h][w][ch] = int(val_y)


img_path = r"../data/lena.jpeg"
src = cv2.imread(img_path)
o_h, o_w, c = src.shape
# use the inter_linear
dst = cv2.resize(src, (1000, 500), interpolation=cv2.INTER_LINEAR)
my_dst = linearInter(src, 1000, 500)
cv2.imshow("original", src)
cv2.imshow("inter", dst)
cv2.imshow("myself", my_dst)
cv2.waitKey(0)