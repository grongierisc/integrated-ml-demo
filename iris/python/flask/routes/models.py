from . import routes
from flask import Flask, jsonify, request, make_response
from humps import camelize
import iris

# ----------------------------------------------------------------
### MODEL MANAGEMENT
# ----------------------------------------------------------------

# ----- MODELS -----

# GET all models
@routes.route("/api/integratedML/ml/models", methods=["GET"])
def getAllModels():
    query = "SELECT * FROM INFORMATION_SCHEMA.ML_MODELS"
    rs = iris.sql.exec(query)
    payload = {}
    # We first take the rs as a dataframe. We then replace the values Nan with "". We camelize the keys of this dataframe (to have camel case, in accord with the swagger). Finally, we convert this dataframe to a dictionary, wde orient that conversion with records so that we have an array with each model as an element.
    payload['models'] = camelize(rs.dataframe().replace({float("Nan"): ""}).to_dict(orient="records"))
    payload['query'] = query
    return jsonify(payload)

# POST new model
@routes.route("/api/integratedML/ml/models", methods=["POST"])
def createModel():
    createInfo = request.get_json()
    query = "CREATE MODEL " + createInfo['modelName'] + " PREDICTING(" + createInfo['predictValue'] + ")"
    if ('withVariables' in createInfo):
        query += " WITH("
        varIter = iter(createInfo['withVariables'])
        query += varIter.__next__()
        for var in varIter:
            query += ", " + var
        query += ")"
    query += " FROM " + createInfo['fromTable']
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

# DELETE model by name
@routes.route("/api/integratedML/ml/models", methods=["DELETE"])
def deleteModel():
    query = "DROP MODEL " + request.args.get('modelName')
    try:
        iris.sql.exec(query)
    except:
        return make_response(
            'Not Found',
            204
        )
    payload = {}
    payload['query'] = query
    return jsonify(payload)

# DELETE to purge model
@routes.route("/api/integratedML/ml/models/purge", methods=["DELETE"])
def purgeModel():
    query = "ALTER MODEL " + request.args.get('modelName') + " PURGE ALL"
    try:
        iris.sql.exec(query)
    except:
            return make_response(
                'Not Found',
                204
            )
    payload = {}
    payload['query'] = query
    return jsonify(payload)