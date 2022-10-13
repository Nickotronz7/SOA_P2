# Slim version of Python
FROM python:3.9

USER root


# Download Package Information
RUN apt-get update && apt-get upgrade -y

RUN apt-get update -y
RUN apt-get install -y python-pika-doc

# Install Tkinter
RUN apt-get install tk -y

# Copy the modules
COPY requirements.txt .

# Install the dependencies
RUN pip3 install -r requirements.txt

# Copy the Python app modules
COPY ./app ./app

# Entry command to start the container running the main module
CMD ["python3", "./app/main.py"]



