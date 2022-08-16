import torch
import torchvision

accum_step = 4
optimizer.zero_grad()
for idx, (x, y) in enumerate(train_loader):
    pred = model(x)
    loss = criterion(pred, y)

    loss = loss / accum_step
    loss.backward()

    if (idx+1) % accum_step == 0 or (idx+1) == len(train_loader):
        optimizer.step()
        optimizer.zero_grad()
    if (idx+1) % eval_steps == 0:
        eval()