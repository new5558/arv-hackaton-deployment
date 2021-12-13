import os
import numpy as np
import ast

is_pytorch = ast.literal_eval(os.environ.get('is_pytorch').title())

def tflite_to_bbox(result):
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
            interpreter = tflite.Interpreter("./model/retinanet_resnet50_v1_fpn_640x640_2.tflite")
            my_signature = interpreter.get_signature_runner()
            self.model = my_signature

    def predict(self, img):
        if is_pytorch:
            results = self.model(img)
            result_array = results.pandas().xyxy[0].to_numpy()
            bbox_list = list(map(yolo_to_bbox, result_array))
            return bbox_list
        else:
           detector_output = self.model(input_tensor=img[None])
           bbox_list = tflite_to_bbox(detector_output)
           return bbox_list
           

