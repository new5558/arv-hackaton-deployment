import torch

model = torch.hub.load('ultralytics/yolov5', 'custom', path='./model/yolov5l.pt', device='cpu')