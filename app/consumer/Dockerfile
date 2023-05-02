FROM python:3.9.7

WORKDIR /app/consumer

COPY . /app/consumer

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-dotenv kafka-python
RUN pip install pymongo

CMD [ "python", "consumer.py" ]