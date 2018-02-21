# KEEP THIS FILE TO SHOW HOW TO SET UP PYKAKASI
FROM ubuntu

MAINTAINER Hugbot

RUN apt-get update

# Python 3
RUN apt-get install -y python3
# Pip
RUN apt-get install -y python3-setuptools
RUN apt-get install -y python3-pip
# Git
RUN apt-get install -y git

COPY . /opt/learn_japanese_grader

# TODO: Use virtualenv
RUN pip3 install --upgrade pip

# Needed for pykakasi
RUN pip3 install nose
# Install pykakasi
RUN git clone https://github.com/miurahr/pykakasi /opt/pykakasi
WORKDIR /opt/pykakasi
RUN sed -i "s/_pre_build/prebuild/g" /opt/pykakasi/setup.py 
RUN cat /opt/pykakasi/setup.py
RUN python3 setup.py sdist
RUN pip3 install dist/*
RUN python3 setup.py clean

RUN pip3 install -r /opt/learn_japanese_grader/source_code/requirements.txt

# Run bot
CMD python3 /opt/learn_japanese_grader/source_code/server.py