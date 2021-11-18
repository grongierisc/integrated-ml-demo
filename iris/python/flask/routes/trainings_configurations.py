from . import routes
from flask import Flask, jsonify, request, make_response
from humps import camelize
import iris

# ----- ML CONFIGURATION -----

# GET all configurations
@routes.route("/api/integratedML/ml/trainings/configurations", methods=["GET"])
def getAllConfigurations():
    payload = {}
    payload['configs'] = iris.cls("%SYS.ML.Configuration")._GetListOfAllConfigNames()
    payload['defaultConfigName'] = iris.cls("%SYS.ML.Configuration")._GetSystemDefault()
    return jsonify(payload)

# PUT to change configuration
@routes.route("/api/integratedML/ml/trainings/configurations", methods=["PUT"])
def changeConfiguration():
    configName = request.get_json()    
    try:
        query = "SET ML CONFIGURATION ?"
        iris.sql.exec(query,configName['configName'])
        payload = {}
        payload['query'] = query
    except:
        return make_response(
            'Not Found',
            204
        )
    return jsonify(payload)

# POST new DR configuration
@routes.route("/api/integratedML/ml/trainings/configurations/datarobot", methods=["POST"])
def createDRConfiguration():
    configInfo = request.get_json()
    query = "CREATE ML CONFIGURATION DataRobotConfig PROVIDER DataRobot URL '" + configInfo['url'] + "' APITOKEN '" + configInfo['apiToken'] + "'"
    iris.sql.exec(query)
    payload = {}
    payload['query'] = query
    return jsonify(payload)

# PUT to change DR config
@routes.route("/api/integratedML/ml/trainings/configurations/datarobot", methods=["PUT"])
def alterDRConfiguration():
    configInfo = request.get_json()
    query = "ALTER ML CONFIGURATION DataRobotConfig PROVIDER DataRobot URL '" + configInfo['url'] + "' APITOKEN '" + configInfo['apiToken'] + "'"
    iris.sql.exec(query)
    payload = {}
    payload['query'] = query
    return jsonify(payload)