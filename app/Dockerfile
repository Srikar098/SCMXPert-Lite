FROM python:3.9.7

COPY . /SCMXPertLite/app/main.py

COPY . /SCMXPertLite/app/requirements.txt

WORKDIR /SCMXPertLite/app/main.py

RUN apt-get update && apt-get install -y python3-pip && pip3 install -r requirements.txt

EXPOSE 8000

CMD [ "uvicorn", "main:app", "--reload", "--host=0.0.0.0", "--port=8000"]
