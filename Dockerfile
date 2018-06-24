FROM phusion/basimage

RUN mkdir /src
WORKDIR /src
COPY requirements.txt /src
COPY myMDB/ src/mymdb
COPY scripts/ /mymdb/scripts
RUN mkdir /var/log/mymdb
RUN touch /var/log/mymdb/mymdb.log
