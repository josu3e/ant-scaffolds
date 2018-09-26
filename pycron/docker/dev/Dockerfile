FROM amazonlinux:2018.03

# Install Python, tools and Nginx

RUN yum -y update && yum -y install \
    python35 \
    python35-pip \
    python35-devel \
    gcc

ADD resources /resources/
RUN python35 --version
RUN chmod +x /resources/test.sh

ENV TZ=America/Lima
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /resources/
RUN pip-3.5 install -r ./requirements.txt

# STDOUT LOG
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log

ONBUILD ADD app /app/

WORKDIR /app

EXPOSE 80
ENTRYPOINT /resources/runservices.sh
