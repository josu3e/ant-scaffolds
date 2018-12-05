FROM amazonlinux:2018.03

# Install Python, tools

RUN yum -y update && yum -y install \
    python35 \
    python35-pip \
    python35-devel \
    gcc

ADD resources /resources/
RUN python35 --version

WORKDIR /app

RUN pip3 install -e .

ENTRYPOINT ['pyCLI']