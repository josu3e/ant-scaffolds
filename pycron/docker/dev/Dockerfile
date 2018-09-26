FROM amazonlinux:2018.03

# Install Python, tools and Nginx

RUN yum -y update && yum -y install \
    python35 \
    python35-pip \
    python35-devel \
    gcc

RUN python35 --version

ENV TZ=America/Lima
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip-3.5 install -r /app/{{ package }}/requirements.txt

ONBUILD ADD app /app/

WORKDIR /app

EXPOSE 80
ENTRYPOINT ["python3", "{{ package }}/cli.py"]
