FROM python:3.6.4-alpine3.7

RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk add --no-cache --update gcc python3-dev musl-dev python3 py-pip coreutils bash build-base py-numpy g++ curl

RUN pip3 install bottle numpy cython pandas
COPY . /opt/webapp
WORKDIR /opt/webapp
RUN apk add --no-cache --update libffi-dev openssl-dev
RUN pip install -r requirements.txt
EXPOSE 8080
ENV FLASK_APP app.py
ENV FLASK_DEBUG 1
ENTRYPOINT ["entrypoint.sh"]
# docker build -t bismark:1 . && docker run -it --entrypoint bash -v /var/foo/settings.yml:/opt/webapp/settings.yml -v `pwd`:/opt/webapp -p 8080:8080 bismark:1
