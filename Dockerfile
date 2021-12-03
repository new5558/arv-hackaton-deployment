FROM python:3.8

WORKDIR app

RUN apt-get update && DEBIAN_FRONTEND=noninteractive  apt-get install -y python3-pip libgl1-mesa-dev libglib2.0-0

COPY requirements.txt .
RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt

EXPOSE 8000

COPY . .


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
