import torch
from torchvision import transforms
import numpy as np

# create the tensor
t = np.random.randn(6, 6, 3)
print(t)
# toTensor
trans1 = transforms.ToTensor()
t1 = trans1(t)
print(t1)
# normalize
trans2 = transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
t2 = trans2(t1)
print(t2)