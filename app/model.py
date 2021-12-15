import os
import numpy as np
import ast

is_pytorch = ast.literal_eval(os.environ.get('is_pytorch').title())

def tflite_to_bbox(result):
  converted_result = []
  for i in range(len(result['output_2'][0])): # detection classes
    score = result['output_1'][0].tolist()[i] # dection socre
    if score > 0:
      result_object = {}
      result_object['category_id'] = int(result['output_2'][0].tolist()[i] + 1)
      result_object['score'] = score
      box = result['output_3'][0][i].tolist() # dection boxes
      bbox = {}
      bbox['x'] = box[1] * 1080
      bbox['y'] = box[0] * 1920
      bbox['w'] = (box[3] - box[1]) * 1080
      bbox['h'] = (box[2] - box[0]) * 1920
      result_object['bbox'] = bbox
      converted_result.append(result_object)
  return converted_result

def yolo_to_bbox(array):
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


class Model:
    def __init__(self):
        print(bool(is_pytorch), is_pytorch, 'bool(is_pytorch)')
        if is_pytorch:
            import torch
            self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='./model/yolov5s.pt', device='cpu')
        else:
            import tflite_runtime.interpreter as tflite
            interpreter = tflite.Interpreter("./model/efficientdet-lite-real-augment-50-3.tflite")
            my_signature = interpreter.get_signature_runner()
            self.model = my_signature

    def predict(self, img):
        if is_pytorch:
            results = self.model(img)
            result_array = results.pandas().xyxy[0].to_numpy()
            bbox_list = list(map(yolo_to_bbox, result_array))
            return bbox_list
        else:
           detector_output = self.model(images=img[None])
           bbox_list = tflite_to_bbox(detector_output)
           return bbox_list
           

