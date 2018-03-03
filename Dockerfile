# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /addressblox
WORKDIR /addressblox

# Copy the current directory contents into the container at /addressblox
ADD . /addressblox

ENV PYTHONPATH=src/
ENV APP_NAME=addressblox

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN python setup.py test
