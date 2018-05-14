FROM python:3.6.4-alpine3.7

RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk add --no-cache --update python3 py-pip bash curl nodejs
# RUN pip install --upgrade pip

COPY . /opt/webapp
WORKDIR /opt/webapp
RUN apk add --no-cache --update --virtual .build-deps \
    gcc python3-dev musl-dev coreutils build-base py-numpy g++ libffi-dev openssl-dev \
    && pip3 install cython numpy
RUN pip3 install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

RUN npm install /opt/webapp/client/

RUN ["chmod", "+x", "/opt/webapp/entrypoint.sh"]
EXPOSE 8080 8000
ENV FLASK_APP app.py
ENV FLASK_DEBUG 1
ENTRYPOINT ["/opt/webapp/entrypoint.sh"]

###########
# build locally
###########

# docker build -t danielp16/bismark .
# docker push danielp16/bismark


###########
# on docker machine run rethinkdb + flask
##########
# docker rm --force rethinkdb; docker run -d --name rethinkdb -p 28015:28015 -p 8090:8080 rethinkdb



#########
# pull image and run
########

# docker pull danielp16/bismark
# docker run -it -v ./settings.yml:/opt/webapp/settings.yml -p 8080:8080 --link rethinkdb danielp16/bismark
