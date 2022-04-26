FROM python:3.10.4-slim-buster

RUN mkdir /opt/app
#RUN mkdir /opt/app/input_data
WORKDIR /opt/app
RUN pip install pandas
