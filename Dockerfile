FROM python:3.9.12-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update -y
RUN apt-get upgrade -y
RUN python -m pip install --upgrade pip
COPY requirements.txt /usr/src/app/

WORKDIR /usr/src/app

RUN pip install -r requirements.txt

COPY . /usr/src/app
