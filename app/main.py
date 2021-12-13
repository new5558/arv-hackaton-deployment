from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
import urllib.request
import numpy as np
import cv2
import torch

import os
print(os.environ)
path = os.environ.get('path')
app = FastAPI()
# model = torch.hub.load('ultralytics/yolov5', 'yolov5l', device='cpu')  # default
model = torch.hub.load('ultralytics/yolov5', 'custom', path='./model/yolov5l.pt', device='cpu')

print(path, 'path')

def to_object(array):
  result_object = {}
  result_object['category_id'] = array[5]
  result_object['score'] = array[4]
  bbox = {}
  bbox['x'] = array[0]
  bbox['y'] = array[3]
  bbox['w'] = array[2] - array[0]
  bbox['h'] = array[3] - array[1]
  result_object['bbox'] = bbox
  return result_object


@app.get("/")
def read_root():
    return {"Hello": "World"}


class Payload(BaseModel):
    url: str
    image_id: str

@app.post("/"+path+"/predict")
def predict(payload: Payload): 
  response = urllib.request.urlopen(payload.url)
  img_data = response.read()
  
  arr = np.asarray(bytearray(img_data), dtype=np.uint8)
  img = cv2.imdecode(arr, -1) # 'Load it as it is'
  img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

  results = model(img) 
  result_array = results.pandas().xyxy[0].to_numpy()

  bbox_list = list(map(to_object, result_array))

  return {
    "test": "test",
    "image_id" : payload.image_id,
    "bbox_list": bbox_list
  }

  