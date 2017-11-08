FROM python:3.6

# system requirements install
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y python3-dev

# Add and install Python modules
ADD requirements.txt /src/requirements.txt
RUN cd /src; pip install -r requirements.txt

RUN pip install uwsgi

# Bundle app source
ADD . /src

# Expose
EXPOSE 8668

ENTRYPOINT ["uwsgi", "--http", "0.0.0.0:8668", "--chdir", "/src","--module", "application:application", "--processes", "1", "--threads", "8"]
