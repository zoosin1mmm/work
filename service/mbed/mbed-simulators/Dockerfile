FROM ubuntu:trusty

#=========================================
# Install base
#=========================================
RUN apt-get -y update && \
    apt-get -y dist-upgrade && \
    apt-get -y install curl git

#=========================================
# Install build tools
#=========================================
RUN apt-get -y install build-essential cmake ninja-build clang-3.5

#=========================================
# Install arm gcc
#=========================================
RUN apt-get -y install software-properties-common && \
    add-apt-repository -y ppa:team-gcc-arm-embedded/ppa && \
    apt-get -y update && \
    apt-get -y install gcc-arm-embedded

#=========================================
# Install python
#=========================================
RUN apt-get -y install python python-setuptools python-usb && \
    apt-get -y remove python-pip && \
    easy_install pip

#=========================================
# Install python build requirements
#=========================================
RUN apt-get -y install python-dev libffi-dev libssl-dev libxml2-dev

#=========================================
# Install yotta
#=========================================
RUN pip install -U pyopenssl ndg-httpsclient pyasn1 requests yotta==0.16.4

#=========================================
# Install srecord
#=========================================
RUN apt-get -y install srecord

#=========================================
# Clone mbed-client-linux-example
#=========================================
RUN git clone https://github.com/ARMmbed/mbed-client-linux-example.git

#=========================================
# Workspace
#=========================================
WORKDIR /mbed-client-linux-example
RUN yotta target x86-linux-native
ADD security.tar /mbed-client-linux-example
RUN rm /mbed-client-linux-example/source/main.cpp
ADD main.cpp /mbed-client-linux-example/source
ADD device.py /mbed-client-linux-example
