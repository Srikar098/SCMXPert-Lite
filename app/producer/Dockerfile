FROM python:3.9.7

# Set the working directory to /app/producer
WORKDIR /app/producer

# Copy the current directory contents into the container at /app/producer
COPY . /app/producer

# Install required packages
RUN pip install python-dotenv kafka-python

# Run the producer
CMD [ "python", "producer.py" ]