# Pull Python image from Docker Hub
FROM python:3.8 

WORKDIR /emotions-app

# Copy the modules
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the Python app modules
COPY ./app ./app

# Entry command to start the container running the main module
CMD ["python", "./app/main.py"]
