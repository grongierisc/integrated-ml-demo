#!/bin/bash

set -m

/iris-main "$@" &

/usr/irissys/dev/Cloud/ICM/waitISC.sh

cd ${FLASK_PATH}

${PYTHON_PATH} -m gunicorn --bind "0.0.0.0:8080" wsgi:app &

fg %1