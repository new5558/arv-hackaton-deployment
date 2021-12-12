import torch

model = torch.hub.load('ultralytics/yolov5', 'custom', path='./model/yolov5m.pt', device='cpu')