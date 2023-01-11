FROM python:3.11-slim

RUN mkdir app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD . /app/

ENV PYTHONUNBUFFERED=1

CMD [ "python3.11", "crawler/manage.py runserver 0.0.0.0:8000" ]