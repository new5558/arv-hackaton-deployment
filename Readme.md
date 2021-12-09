#### Example payload:

```javascript
{"url":"https://pngquant.org/Ducati_side_shadow.png","image_id":1}
```

#### Example cURL:

```javascript
curl -X POST \
  http://localhost/new5558/predict \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -d '{"url":"https://pngquant.org/Ducati_side_shadow.png","image_id":1}'
```

#### Response:

```javascript
{
    "image_id" : 1,
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
};
```
