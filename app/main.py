from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Payload(BaseModel):
    url: str
    image_id: str

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/")
def predict(payload: Payload):


  return {
    "image_id" : payload['image_id'],
    "bbox_list": [{
        "category_id": 0,
        "bbox": {
          "x": 0,
          "y": 220.66666666666669, 
          "w": 1050.0986882341442,
          "h": 525.3333333333333
          },
        "score": 0.63508011493555
      },{
        "category_id": 1,
        "bbox": {
          "x": 0,
          "y": 220.66666666666669, 
          "w": 1050.0986882341442,
          "h": 525.3333333333333
          },
        "score": 0.63508011493555
      }]
    }