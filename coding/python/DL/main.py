import numpy as np

# calculate the nms
def calIou():
    pass

# after the prediction, we get the matrix, preds = n x 5
n = 10
preds = np.random.random((10, 5))
print(preds)
# sort the preds
args_ls = list(np.argsort(preds[:, -1]))

print(preds[args_ls])
ans = list()
iou_threshold = 0.5
conf_thres = 0.5
# drop the id that the confidence smaller than the conf_thres
for i in range(len(args_ls)-1, -1, -1):
    if (preds[args_ls[i], -1] < conf_thres):
        args_ls.pop(i)
#
while len(args_ls) > 0:
    # first get the bbox and then put it to the ans
    select_id = args_ls[0]
    select_bbox = preds[select_id]
    ans.append(select_bbox)
    # if the len is 1, that no need to cal the iou, just select the bounding box and then break the loop
    if len(preds) == 1:
        break
    # calculate the IoU, if the IoU > IoU_threshold, drop it out.
    for i in range(len(preds)-1, -1):
        if calIou(select_bbox, preds[i]) > iou_threshold:
            pass
            # do something
print("the answer is the: ")
print(ans)