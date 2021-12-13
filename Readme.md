#### Example payload:

```javascript
{"url":"https://arken.finance/images/decorations/hero-web.png","image_id":1}
```

### Example cURL:    

Localhost
```javascript
curl -X POST \
  http://localhost:3000/new5558/predict \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -d '{"url":"https://arken.finance/images/decorations/hero-web.png","image_id":1}'
```

Staging (AWS ECS)
```javascript
curl -X POST \
  http://18.139.138.231/new5558/predict \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -d '{"url":"https://arken.finance/images/decorations/hero-web.png","image_id":1}'
```

### Response:

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

### Local build with docker
```docker build -f Dockerfile-tflite -t arv-lite .```
```docker run --name arv-lite -p 3000:80 arv-lite```
