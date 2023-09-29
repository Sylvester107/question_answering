# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY  . /app

# Install any needed packages in requirements.txt
RUN pip install pip install --no-cache-dir --upgrade -r requirements.txt

# Make port 7000-8000 available 
EXPOSE 7000-8000

# Define the command to run the Flask app
CMD ["py", "app/app.py"]
