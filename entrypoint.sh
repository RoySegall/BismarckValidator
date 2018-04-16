#!/usr/bin/env bash

! [ -e settings.yml ] && echo missing settings.yml && exit 1
! python install.py && echo failed to setup DB && exit 1
echo starting flask
flask run --port ${FLASK_PORT:-8080}
