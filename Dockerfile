FROM python:3.8
WORKDIR /home/root

# Requirements
COPY requirements.txt /home/root
RUN pip install -r requirements.txt
