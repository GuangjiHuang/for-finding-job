import numpy as np
import cv2
import torch
import torch.nn as nn
import torchvision

# first step: build the module
class MyNet(nn.Module):
    def __init__(self):
        super().__init()
        pass

    def forward(self):
        pass
# second step: build the loss
class MyLoss(nn.Module):
    def __init__(self):
        super().__init__()

    def forwar(self):
        pass

# the thrid step: the optimizer;

# train
def train():
    # build the dataSet class

    # build the dataLoader class, use the dataset to construct the dataLoader

    train_loader = ()
    #
    epoches = 100
    for epoch in range(epoches):
        # the batch size, use the dataLoader, we can get the batch data
        for i, x in enumerate(train_loader):
            # optimizer zero gradience
            my_optimizer.zero_grad()
            # forward propagation
            out = MyNet(x)
            # calculate the loss
            loss = MyLoss(out, ...)
            # backward propagation
            loss.backward()
            # update the weights.
            optimizer.step()
        # for each epoch, we can validate our module, or you can test

# test
def test():
    # first we should build the test_dateSet and the testLoader
    # and then we get the image
    test_loader = ()
    test_data = test_loader
    # get the output of the
    output = modlue(test_data)
    # and then get the result, the recall, precision, or the mAP, or the F1-score, or the others to see the module's ability
    # decode the output, and then compare with the ground truth, have to count the IOU, have to get the recall, and have to get the precision and so on.
    ....
    # and then we get the test result.










































