FROM python:3.8
WORKDIR /app

# Requirements
COPY requirements.txt /app
RUN pip install -r requirements.txt
