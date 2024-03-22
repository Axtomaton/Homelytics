# Use an official Python runtime as the base image
FROM python:3.12.2

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory for the app
WORKDIR /homelytics

# Copy requirements.txt separately to leverage Docker cache
COPY homelytics/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY homelytics/ .

# Set the working directory for the backend
WORKDIR /homelytics/backend

# Run the Python script
CMD ["python", "main.py"]
