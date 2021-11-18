from . import routes
from flask import Flask, jsonify, request, make_response
import iris

# ----------------------------------------------------------------
### ADDITIONAL METHODS FOR ALL TABLES
# ----------------------------------------------------------------

# GET the size of a table
@routes.route("/api/integratedML/ml/tablesize", methods=["GET"])
def getTableSize():
    query = "SELECT COUNT(*) FROM " + request.args.get('table')
    try:
        rs = iris.sql.exec(query)
    except:
        return make_response(
            'Not Found',
            204
        )
    total = rs.__next__()   
    return jsonify({'total': total[0]})