# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1

VOLUME [ "/code" ]

WORKDIR /code

RUN pip install pandas
RUN pip install numpy
RUN pip install spacy

# COPY requirements.txt /code/
# RUN pip install -r requirements.txt
# COPY . /code/

# RUN sudo chown -R $USER:$USER .
