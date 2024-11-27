FROM python:3

ENV PYTHONBUFFERED 1
RUN mkdir /ShoppieBackend
WORKDIR /ShoppieBackend
COPY . /ShoppieBackend/
RUN pip install -r requirements.txt