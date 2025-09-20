# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . /app 

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5000

# Run Flask
CMD ["python", "./app.py"]
