# Pull Python image from Docker Hub
FROM ubuntu:latest

RUN apt update
RUN apt install python3 -y
RUN apt install python3-pip -y

WORKDIR /addui-app

# Copy the modules
COPY requirements.txt .

# Install the dependencies
RUN pip3 install -r requirements.txt

# Copy the Python app modules
COPY ./app/event_processor.py /app/event_processor.py
COPY ./app/index_strings.py /app/index_strings.py
COPY ./app/index1.html /app/index1.html
COPY ./app/index2.html /app/index2.html
COPY ./app/main.py /app/main.py

# Entry command to start the container running the main module
CMD ["python3", "/app/main.py"]
