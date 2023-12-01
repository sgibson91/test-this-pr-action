# Use a Python 3.9 slim image
FROM python:3.12.0-slim

# Create and set the 'app' working directory
RUN mkdir /app
WORKDIR /app

# Copy repository contents into the working directory
COPY . /app

# Upgrade pip and install dependencies
RUN pip install -U pip && pip install -r /app/requirements.txt

# Make main.py executable
RUN ["chmod", "+x", "/app/src/main.py"]

# Set entrypoint
ENTRYPOINT ["python", "/app/src/main.py"]
