from . import routes
from flask import Flask, jsonify, request, make_response
from humps import camelize
import iris

# ----- TRAINED MODELS -----

# GET all trained models
@routes.route("/api/integratedML/ml/predictions/models", methods=["GET"])
def getTrainedModels():
    query = "SELECT * FROM INFORMATION_SCHEMA.ML_TRAINED_MODELS"
    rs = iris.sql.exec(query)
    payload = {}
    payload['models'] = camelize(rs.dataframe().replace({float("Nan"): ""}).to_dict(orient="records"))
    payload['query'] = query
    return jsonify(payload)

# GET prediction for an id from a certain trained model and a certain table
@routes.route("/api/integratedML/ml/predictions", methods=["GET"])
def predict():
    query = "SELECT PREDICT(" + request.args.get('model') + " USE " + request.args.get('trainedModel') + ") FROM " + request.args.get('fromTable') + " WHERE ID = ?"
    try:
        rs = iris.sql.exec(query, request.args.get('id'))
    except:
        return make_response(
            'Bad Request',
            400
        )
    payload = {}
    payload['predictedValue'] = rs.__next__()[0]
    payload['query'] = query
    return jsonify(payload)

# GET probability
@routes.route("/api/integratedML/ml/predictions/probabilities", methods=["GET"])
def probability():
    query = "SELECT PROBABILITY(" + request.args.get('model') + " USE " + request.args.get('trainedModel') + " FOR " + request.args.get('labelValue') + ") FROM " + request.args.get('fromTable') + " WHERE ID = ?"
    try:
        rs = iris.sql.exec(query, request.args.get('id'))
    except:
        return make_response(
            'Bad Request',
            400
        )
    payload = {}
    payload['probability'] = rs.__next__()[0]
    payload['query'] = query
    return jsonify(payload)