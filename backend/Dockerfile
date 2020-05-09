# Use an official Python runtime as a parent image
FROM python:3.7
ENV PYTHONBUFFERED 1

# Adding backend directory to make absolute filepaths consistent across services
RUN mkdir /code
WORKDIR /code

# Install Python dependencies
COPY requirements.txt /code

RUN pip install -r requirements.txt
RUN pip install docker-compose
RUN pip install celery

# Add the rest of the code
COPY . /code/
