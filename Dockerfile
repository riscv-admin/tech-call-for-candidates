# Use an official Python runtime as the base image
FROM python:3.8-slim

# Environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=9002

ENV GITHUB_TOKEN=""
ENV GITHUB_USER=""
ENV FLASK_SECRET_KEY=""

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run gunicorn
CMD ["gunicorn", "-w", "4", "-b", ":9002", "app:app"]