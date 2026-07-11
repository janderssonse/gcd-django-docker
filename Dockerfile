# syntax=docker/dockerfile:1
FROM python:3.13
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set work directory
RUN mkdir /code
WORKDIR /code
# install external packages
RUN apt-get update && apt-get install -y vim
COPY gcd-django/requirements.txt .
RUN pip install -r requirements.txt
COPY gcd-django gcd-django
COPY setup_initial_changesets.py .
COPY settings_local.py /code/gcd-django/
