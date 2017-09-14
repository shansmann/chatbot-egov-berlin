FROM continuumio/anaconda3

RUN apt-get -y update

# Add and install Python modules
ADD requirements.txt /src/requirements.txt
RUN cd /src; pip install -r requirements.txt

# Bundle app source
ADD . /src

# Expose
EXPOSE 8085

# uWSGI install
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y python3-dev
RUN pip install uwsgi

# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
# COPY uwsgi.ini /etc/uwsgi/

ENTRYPOINT ["uwsgi", "--http", "0.0.0.0:8085", "--chdir", "/src","--module", "application:application", "--processes", "1", "--threads", "8", "--master"]
