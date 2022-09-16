import torch
import torch_geometric
print(torch.__version__)
print(torch_geometric.__version__)

print(f"cuda avail: {torch.cuda.is_available()}")
print(f"cudnn avail: {torch.backends.cudnn.is_available()}")
print(f"device count: {torch.cuda.device_count()}")

for idx in range(torch.cuda.device_count()):
    print(f"device: {torch.cuda.device(idx)}")
    print(f"device name: {torch.cuda.get_device_name(idx)}")
