# FROM python:3.8-alpine

# WORKDIR app

# RUN apt-get update && DEBIAN_FRONTEND=noninteractive  apt-get install -y python3-pip libgl1-mesa-dev libglib2.0-0

# COPY requirements.txt .
# RUN pip3 install --upgrade pip \
#     && pip3 install -r requirements.txt

# RUN pip3 install pandas
# RUN pip3 install Image pyyaml tqdm
# RUN pip3 install torchvision
# RUN pip3 install matplotlib seaborn

# ENV path new5558

# EXPOSE 80

# COPY . .


# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]


FROM tiangolo/uvicorn-gunicorn:python3.8-slim
ENV path new5558

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./app /app
