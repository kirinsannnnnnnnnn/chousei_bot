# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV YOUR_CHANNEL_ACCESS_TOKEN=4GCUcgKPRy44Bf0OOF+tw8a0GZjeFljbJHU0lHTUhlrQKr4UQibg9jFdvgOIJn2j0WwASOAQG+zLl/83ldS6vT7TaqW6B/Ajuj2cOPFxerFNOyh/dPZbpPeveDGvQtPKJtJlvLrjfJb4BGA0w5/FTAdB04t89/1O/w1cDnyilFU=
ENV YOUR_CHANNEL_SECRET=9d82e2bbcfbd8fe0c757d5fb682c4b7c

# Make port 80 available to the world outside this container
EXPOSE 8080 80

# Run app.py when the container launches
CMD ["python", "-u", "manage.py"]
