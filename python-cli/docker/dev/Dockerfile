FROM amazonlinux:2018.03

# Install Python, tools

RUN yum -y update && yum -y install \
    python35 \
    python35-pip \
    python35-devel \
    gcc

ADD docker/dev/resources /resources/
RUN python35 --version

ADD . /app
WORKDIR /app
RUN pip-3.5 install -e .

ENTRYPOINT ['pyCLI']