from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
import urllib.request
import numpy as np
import cv2
from .model import Model

import os
print(os.environ)
path = os.environ.get('path')
app = FastAPI()
print(path, 'path')

model = Model()

@app.get("/"+path)
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

  bbox_list = model.predict(img)

  return {
    "image_id" : payload.image_id,
    "bbox_list": bbox_list
  }

  