FROM phusion/basimage

RUN mkdir /src
WORKDIR /src
COPY requirements.txt /src
COPY myMDB/ src/mymdb
COPY scripts/ /mymdb/scripts
RUN mkdir /var/log/mymdb
RUN touch /var/log/mymdb/mymdb.log

RUN apt-get -y update
RUN apt-get install -y nginx postgresql-client python3 python3-pip
RUN pip3 install virtualenv
RUN virtualenv /mymdb/venv
RUN bash /mymdb/scripts/pip_install.sh /mymdb
