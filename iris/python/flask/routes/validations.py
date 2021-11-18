from . import routes
from flask import Flask, jsonify, request, make_response
from humps import camelize
import iris

# ----- VALIDATION RUNS -----

# GET all validation runs
@routes.route("/api/integratedML/ml/validations", methods=["GET"])
def getValidationRuns():
    query = "SELECT MODEL_NAME, TRAINED_MODEL_NAME, VALIDATION_RUN_NAME, START_TIMESTAMP, COMPLETED_TIMESTAMP, VALIDATION_DURATION, RUN_STATUS, STATUS_CODE, SETTINGS, VALIDATION_RUN_QUERY FROM INFORMATION_SCHEMA.ML_VALIDATION_RUNS"
    rs = iris.sql.exec(query)
    payload = {}
    # Standard operational procedure 
    payload['validationRuns'] = camelize(rs.dataframe().replace({float("Nan"): ""}).to_dict(orient="records"))
    # TODO: same than training runs with the logs
    payload['query'] = "SELECT * FROM INFORMATION_SCHEMA.ML_VALIDATION_RUNS"
    return jsonify(payload)

# POST new validation run
@routes.route("/api/integratedML/ml/validations", methods=["POST"])
def validateModel():
    validationInfo = request.get_json()
    query = "VALIDATE MODEL " + validationInfo['modelName'] 
    if ('validationName' in validationInfo):
        query += " AS " + validationInfo['validationName'] 
    query += " USE " + validationInfo['trainedModelName'] + " FROM " + validationInfo['fromTable']
    try: 
        iris.sql.exec(query)
    except:
        return make_response(
            'Bad Request', 
            400
        )
    payload = {}
    payload['query'] = query
    return jsonify(payload)

# GET metrics for a validation run
@routes.route("/api/integratedML/ml/validations/metrics", methods=["GET"])
def getMetrics():
    query = "SELECT METRIC_NAME, METRIC_VALUE, TARGET_VALUE FROM INFORMATION_SCHEMA.ML_VALIDATION_METRICS WHERE (VALIDATION_RUN_NAME='" + request.args.get('validationName') + "' AND MODEL_NAME='" + request.args.get('modelName') + "')"
    try:
        rs = iris.sql.exec(query)
    except:
        return make_response(
            'Not Found',
            204
        )
    payload = {}
    # Same as always
    payload['metrics'] = camelize(rs.dataframe().replace({float("Nan"): ""}).to_dict(orient="records"))
    payload['query'] = query
    return jsonify(payload)