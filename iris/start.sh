#!/bin/sh

cd /opt/irisapp/python

/usr/irissys/bin/irispython /usr/irissys/bin/gunicorn --bind 0.0.0.0:8080 wsgi:app >/tmp/flask.log 2>&1 &

exit