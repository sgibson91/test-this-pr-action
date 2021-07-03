# Use a Python 3.9 slim image
FROM python:3.9-slim

# Create and set the 'app' working directory
RUN mkdir /app
WORKDIR /app

# Copy repository contents into the working directory
COPY . /app

# Upgrade pip and install dependencies
RUN pip install -U pip && pip install -r /app/requirements.txt

# Set command and entrypoint
CMD ["/app/src/main.py"]
ENTRYPOINT ["python"]
