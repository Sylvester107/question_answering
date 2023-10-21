# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY  app/app.py /app

# copy the requirements file
COPY requirements.txt /app

# Install any needed packages in requirements.txt
RUN pip install  -r requirements.txt

#Expose port
EXPOSE 5000
# Define the command to run the Flask app
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
