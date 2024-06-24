# FROM python:3.8.10-slim

# WORKDIR /app

# COPY . /app

# RUN pip install -r requirements.txt

# # EXPOSE 80
# # CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]


# Use an official Python runtime as a parent image
# FROM python:3.9-slim

# # Set the working directory to /app
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Install any needed packages specified in requirements.txt
# RUN pip install -r requirements.txt

# # Make port 80 available to the world outside this container
# EXPOSE 80

# # Define environment variable
# ENV NAME World

# # Run app.py when the container launches
# CMD ["python", "app.py"]

# Use the official FastAPI image with Python 3.9
FROM python:3.8.10-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Command to run the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
