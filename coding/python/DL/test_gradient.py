import torch
import torchvision

# the variant
x = torch.tensor(1.0, requires_grad=True)
y = 2 * x + 1
y.retain_grad()
z = y ** 2
z.retain_grad()
loss = 1 - z
loss.retain_grad()
print(z)
# before backward
print("before backward:")
print(f"x's gradient: {x.grad}")
print("----------------------------------------")
loss.backward()
print("after backward:")
print(f"x's gradient: {x.grad}")
print(f"y gradient: {y.grad}")
print(f"z gradient: {z.grad}")
print(f"loss gradient: {loss.grad}")