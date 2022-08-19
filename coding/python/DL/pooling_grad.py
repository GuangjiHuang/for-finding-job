import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import numpy as np

#
x = [[[1, 2, 0, 2], [1, 2, 3, 4], [0, 1, 2, 4], [2, 4, 3, 1]]]
x = torch.tensor(x, dtype=torch.float32, requires_grad=True)

print(x)

# th pooling function
y = F.avg_pool2d(x, 2, stride=1)
#y = F.max_pool2d(x, 2, stride=1)
y.retain_grad()
z = torch.sum(y)
print(y)

# backward the y
print("backward the y:")
z.backward()
print(x.grad)
print(y.grad)