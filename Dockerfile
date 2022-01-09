FROM python:rc-buster
#FROM python:3.8.3-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

RUN pip3 install -r requirements.txt

COPY .  /code