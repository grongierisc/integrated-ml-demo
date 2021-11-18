from flask import Flask, jsonify, request, make_response
from flask_cors import CORS

from definitions.patient import Patient
from routes import *


app = Flask(__name__)
CORS(app)
app.register_blueprint(routes)


# ----------------------------------------------------------------
### MAIN PROGRAM
# ----------------------------------------------------------------

if __name__ == '__main__':
    app.run('0.0.0.0', port = "8081")