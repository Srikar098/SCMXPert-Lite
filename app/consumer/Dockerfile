FROM python:3.9.7

# Set the working directory to /app/consumer
WORKDIR /app/consumer

# Copy the current directory contents into the container at /app/consumer
COPY . /app/consumer

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-dotenv kafka-python pymongo

# Run the consumer
CMD [ "python", "consumer.py" ]