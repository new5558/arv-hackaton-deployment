from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
import urllib.request
import requests
import numpy as np
import cv2

import os
print(os.environ)
path = os.environ.get('path')
app = FastAPI()

print(path, 'path')


@app.get("/")
def read_root():
    return {"Hello": "World"}


class Payload(BaseModel):
    url: str
    image_id: str
@app.post("/"+path+"/predict")
def predict(payload: Payload):
  print(type(payload), payload, 'payload')

  # img_data = requests.get(payload.url).content

 
  response = urllib.request.urlopen(payload)
  img_data = response.read()
  
  arr = np.asarray(bytearray(img_data), dtype=np.uint8)
  img = cv2.imdecode(arr, -1) # 'Load it as it is'


  return {
    "image_id" : payload.image_id,
    "bbox_list": [{
        "category_id": 0,
        "bbox": {
          "x": 0,
          "y": 220.66666666666669, 
          "w": 1050.0986882341442,
          "h": 525.3333333333333
          },
        "score": 0.63508011493555
      }]
    }