FROM python:3.9.7

# Set the working directory to /app/socket
WORKDIR /app/socket

# Copy the current directory contents into the container at /app/socket
COPY . /app/socket

# Install required packages
RUN pip install pytz

# Expose port 8085 for the API
EXPOSE 5050

# Run the socket server
CMD [ "python", "server.py" ]