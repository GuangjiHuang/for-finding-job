import torch
import numpy as np
import torch.nn.functional as F

# the input
i_img = torch.randn((1, 1, 13, 13))
weight = torch.randn((1, 3, 3, 3))
#
o_img = F.conv_transpose2d(i_img, weight, stride=2, padding=1)

print(f"the shape of the input is the: {i_img.shape}")
print(f"the shape of the output is the: {o_img.shape}")

