FROM python:3.8-slim-buster

# COPY requirements.txt requirements.txt

VOLUME [ "/code" ]

# COPY . .

# WORKDIR /app

WORKDIR /code

RUN ls

RUN pip3 install django

# RUN pip3 install -r requirements.txt

CMD [ "sh", "-c", "pip3 install -r requirements.txt && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:5000"]
