FROM ubuntu

MAINTAINER Hugbot

RUN apt-get update

# Python 3
RUN apt-get install -y python3
# Pip
RUN apt-get install -y python3-setuptools
RUN apt-get install -y python3-pip

RUN pip3 install -r /opt/learn_japanese_grader/source_code/requirements.txt

# Run bot
CMD python3 /opt/learn_japanese_grader/source_code/server.py