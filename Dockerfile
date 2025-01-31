# Use an official Python runtime as a parent image for building dependencies
FROM python:3.9 AS builder

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target /app/deps

# Use a smaller Python image for the final runtime
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install google.generativeai in the final stage
RUN pip install --no-cache-dir google-generativeai gunicorn

# Copy only necessary files from the builder stage
COPY --from=builder /app/deps /usr/local/lib/python3.9/site-packages
COPY . /app

# Expose the port the app runs on
EXPOSE 5000

# Define environment variable to avoid buffering in logs
ENV PYTHONUNBUFFERED=1

# Run the application using Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
