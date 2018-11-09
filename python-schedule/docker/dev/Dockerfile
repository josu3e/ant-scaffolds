FROM amazonlinux:2018.03

# Install Python, tools

RUN yum -y update && yum -y install \
    python35 \
    python35-pip \
    python35-devel \
    gcc

ADD resources /resources/
RUN python35 --version
ENV LC_ALL=en_US.UTF-8
ENV TZ=America/Lima
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ONBUILD ADD . /app/

WORKDIR /app
