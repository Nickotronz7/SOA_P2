# Slim version of Python
FROM python:3.9

# Download Package Information
RUN apt-get update -y

RUN apt install python3-pip -y

# Install Tkinter
RUN apt-get install tk -y

# Copy the modules
COPY requirements.txt .

# Install the dependencies
RUN pip3 install -r requirements.txt

# Copy the Python app modules
COPY ./app ./app

# Entry command to start the container running the main module
CMD ["\app\main.py"]

ENTRYPOINT ["python3"]
