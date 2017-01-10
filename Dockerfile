FROM resin/rpi-raspbian
MAINTAINER Jerome MOREAU

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install wget git ca-certificates bzip2 build-essential

RUN apt-get install -y python3 python3-pip

ADD . /TickRecorder

WORKDIR /TickRecorder

RUN pip3 install -r requirements.txt

EXPOSE 80
ENTRYPOINT python3 server.py