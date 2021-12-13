FROM python:3.8-slim

WORKDIR app


COPY requirements.txt .
RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt

RUN pip install https://github.com/google-coral/pycoral/releases/download/v2.0.0/tflite_runtime-2.5.0.post1-cp38-cp38-linux_x86_64.whl

ENV path new5558

EXPOSE 80

COPY . .


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
