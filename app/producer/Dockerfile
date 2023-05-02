FROM python:3.9.7

WORKDIR /app/producer

COPY . /app/producer

RUN pip install python-dotenv kafka-python

CMD [ "python", "producer.py" ]