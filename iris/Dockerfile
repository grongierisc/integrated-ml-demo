ARG IMAGE=containers.intersystems.com/intersystems/iris-ml-community:2021.2.0.617.0

FROM $IMAGE

USER root

#COPY key/community.key /usr/irissys/mgr/iris.key

# Update package and install sudo
RUN apt-get update && apt-get install -y \
	nano \
	python3-pip \
	sudo && \
	/bin/echo -e ${ISC_PACKAGE_MGRUSER}\\tALL=\(ALL\)\\tNOPASSWD: ALL >> /etc/sudoers && \
	sudo -u ${ISC_PACKAGE_MGRUSER} sudo echo enabled passwordless sudo-ing for ${ISC_PACKAGE_MGRUSER}

WORKDIR /opt/irisapp
RUN chown ${ISC_PACKAGE_MGRUSER}:${ISC_PACKAGE_IRISGROUP} /opt/irisapp
USER ${ISC_PACKAGE_MGRUSER}
COPY . /opt/irisapp

# load demo stuff
RUN iris start IRIS \
	&& iris session IRIS < /opt/irisapp/iris.script && iris stop IRIS quietly

ENV PYTHON_PATH=/usr/irissys/bin/irispython
ENV PIP_PATH=/usr/irissys/bin/irispip
ENV FLASK_PATH=/opt/irisapp/python/flask
ENV IRISUSERNAME "SuperUser"
ENV IRISPASSWORD $IRIS_PASSWORD

RUN ${PYTHON_PATH} -m pip install -r ${FLASK_PATH}/requirements.txt
