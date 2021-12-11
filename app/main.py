from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
import urllib.request
import numpy as np
import cv2
import tensorflow_hub as hub

import os
print(os.environ)
path = os.environ.get('path')
app = FastAPI()
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s', device='cpu')  # default
# loaded = torch.jit.load('./yolov5s.torchscript')
detector = hub.load("./model/task-definition.json")

print(path, 'path')

def to_object(result):
  converted_result = []
  for i in range(len(result['detection_classes'][0])):
    score = np.array(result['detection_scores'][0]).tolist()[i]
    if score > 0.5:
      result_object = {}
      result_object['category_id'] = np.array(result['detection_classes'][0]).tolist()[i]
      result_object['score'] = score
      box = np.array(result['detection_boxes'][0][i]).tolist()
      bbox = {}
      bbox['x'] = box[0]
      bbox['y'] = box[3]
      bbox['w'] = box[2] - box[0]
      bbox['h'] = box[3] - box[1]
      result_object['bbox'] = bbox
      converted_result.append(result_object)
  print(converted_result)
  return converted_result


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

  detector_output = detector(img[None])
  # class_ids = detector_output["detection_classes"]


  # img_tensor = torch.Tensor(img)
  # results = loaded(img_tensor) 
  # print(results, 'results')
  # result_array = results.pandas().xyxy[0].to_numpy()

  bbox_list = to_object(detector_output)

  return {
    "image_id" : payload.image_id,
    "bbox_list": bbox_list
  }