FROM python:3.9.7

# Set the working directory to /app
WORKDIR /app

# copy requirements.txt file from the current directory of the host machine inside the Docker image
COPY ./requirements.txt /app/requirements.txt

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 8085 for the API
EXPOSE 8085

# Set the entrypoint
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8085"]
