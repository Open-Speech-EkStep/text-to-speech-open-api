FROM nvidia/cuda:11.4.1-devel-ubuntu18.04


ARG DEBIAN_FRONTEND=noninteractive

RUN mkdir /opt/api_dependencies/
WORKDIR /opt/api_dependencies/
COPY installer.sh /opt/api_dependencies/
RUN sh /opt/api_dependencies/installer.sh

