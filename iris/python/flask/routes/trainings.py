from flask.json import dumps
from . import routes
from flask import Flask, jsonify, request, make_response
from humps import camelize
import threading
import iris

# ----- TRAINING RUNS -----

# GET all training runs
@routes.route("/api/integratedML/ml/trainings", methods=["GET"])
def getTrainingRuns():
    query = "SELECT MODEL_NAME, TRAINING_RUN_NAME, PROVIDER, START_TIMESTAMP, COMPLETED_TIMESTAMP, TRAINING_DURATION, RUN_STATUS, STATUS_CODE, SETTINGS, ML_CONFIGURATION_NAME, TRAINING_RUN_QUERY FROM INFORMATION_SCHEMA.ML_TRAINING_RUNS"
    rs = iris.sql.exec(query)
    payload = {}
    # Same procedure than with getting all models
    payload['trainingRuns'] = camelize(rs.dataframe().replace({float("Nan"): ""}).to_dict(orient="records"))
    # TODO: if streams accepted, change the query actually done and add logs back
    payload['query'] = "SELECT * FROM INFORMATION_SCHEMA.ML_TRAINING_RUNS"
    return jsonify(payload)

# POST new training
@routes.route("/api/integratedML/ml/trainings", methods=["POST"])
def trainModel():
    trainingInfo = request.get_json()

    if 'configName' in trainingInfo :
        query = "SET ML CONFIGURATION ?"
        iris.sql.exec(query,trainingInfo['configName'])

    query = "TRAIN MODEL " + trainingInfo['modelName'] + " AS " + trainingInfo['trainingName'] + " FROM " + trainingInfo['fromTable']
    # Use of threading to train the model in background
    # We use the already implemented objecscript method executeQuery() in the IntegratedML.REST.impl.
    iris.cls("IntegratedML.REST.impl").trainModel(dumps(trainingInfo))

    payload = {}
    payload['query'] = query
    return jsonify(payload)

# GET the state of a training run
@routes.route("/api/integratedML/ml/trainings/states", methods=["GET"])
def getStateTrainingRun():
    query = "SELECT RUN_STATUS FROM INFORMATION_SCHEMA.ML_TRAINING_RUNS WHERE TRAINING_RUN_NAME=? AND MODEL_NAME=?"
    rs = iris.sql.exec(query, request.args.get('trainingName'), request.args.get('modelName'))
    payload = {}
    try:
        payload['state'] = rs.__next__()[0]
    except:
        # Since the model is not listed at the beginning of its training, we return an empty string.
        # (That means no 204, Not Found)
        payload['state'] = ""
    payload['query'] = query
    return jsonify(payload)

# GET log for a training run
@routes.route("/api/integratedML/ml/trainings/logs", methods=["GET"])
def getLogTrainingRun():
    query = "SELECT substring(LOG,1,CHAR_LENGTH(LOG)) FROM INFORMATION_SCHEMA.ML_TRAINING_RUNS WHERE TRAINING_RUN_NAME = ?"
    rs = iris.sql.exec(query, request.args.get('trainingName'))
    payload = {}
    payload['log'] = rs.__next__()[0]
    payload['query'] = query
    return jsonify(payload)