# Pull Python image from Docker Hub
FROM ubuntu:latest

RUN apt update
RUN apt install python3 -y
RUN apt install python3-pip -y

WORKDIR /emotions-app

# Copy the modules
COPY requirements.txt .

# Install the dependencies
RUN pip3 install -r requirements.txt

# Copy the Python app modules
COPY ./app ./app

# Entry command to start the container running the main module
CMD ["python3", "./app/main.py"]
