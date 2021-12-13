FROM python:3.8-slim

WORKDIR app

# RUN apt-get update && DEBIAN_FRONTEND=noninteractive  apt-get install -y python3-pip libgl1-mesa-dev libglib2.0-0
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

COPY requirements.txt .
RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt
RUN pip install torch torchvision -f https://torch.kmtea.eu/whl/stable.html

ENV path new5558

EXPOSE 80

COPY . .

RUN python3 app/load_model.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
