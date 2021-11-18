from . import routes
from definitions.patient import Patient
from flask import Flask, jsonify, request, make_response
import iris

# ----------------------------------------------------------------
### CRUD FOR NOSHOW_TABLE.APPOINTMENT
# ----------------------------------------------------------------

# GET all patients, same as for passengers
@routes.route("/api/integratedML/patients", methods=["GET"])
def getAllPatients():
    query = "SELECT ID, * FROM Noshow_Table.Appointment"
    id = request.args.get('id')
    currPage = request.args.get('currPage')
    pageSize = request.args.get('pageSize')
    # Search by name 
    if not (id is None):
        query += " WHERE ID = ?"
        rs = iris.sql.exec(query, id)
    else:
        # Paginator
        if not (currPage is None or pageSize is None):
            currPage = int(currPage)
            pageSize = int(pageSize)
            query += " WHERE ID > ? AND ID <= ?"
            rs = iris.sql.exec(query, pageSize * (currPage - 1), pageSize * currPage)
        # All patients
        else:
            rs = iris.sql.exec(query)
    payload = {}
    payload['patients'] = []
    for p in rs:
        payload['patients'].append(Patient(p).__dict__)
    rs = iris.sql.exec("SELECT MAX(ID) FROM Noshow_Table.Appointment")
    payload['maxId'] = rs.__next__()[0]
    payload['query'] = query
    return jsonify(payload)

# POST new patient, same as for passengers
@routes.route("/api/integratedML/patients", methods=["POST"])
def createPatient():
    patient = request.get_json()
    query = "INSERT INTO Noshow_Table.Appointment (gender, scheduledDay, scheduledHour, appointmentDay, age, neighborhood, scholarship, hypertension, diabetes, alcoholism, handicap, smsReceived, noShow) VALUES (?, DATE(?), ?, DATE(?), ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    newId = int(iris.sql.exec("SELECT MAX(ID) FROM Noshow_Table.Appointment").__next__()[0]) + 1
    try:
        iris.sql.exec(query, patient['gender'], patient['scheduledDay'], patient['scheduledHour'], patient['appointmentDay'], patient['age'], patient['neighborhood'], patient['scholarship'], patient['hypertension'], patient['diabetes'], patient['alcoholism'], patient['handicap'], patient['smsReceived'], patient['noShow'])
    except:
        return make_response(
            'Bad Request',
            400
        )
    payload = {
        'query': query,
        'patientId': newId
    }
    return jsonify(payload)

# GET patient with id, same as for passengers
@routes.route("/api/integratedML/patients/<int:id>", methods=["GET"])
def getPatient(id):
    payload = {}
    query = "SELECT ID, * FROM Noshow_Table.Appointment WHERE ID = ?"
    rs = iris.sql.exec(query, str(id))
    try:
        patient = Patient(rs.__next__()).__dict__
    except:
        return make_response(
            'Not Found',
            204
        )
    payload['patient'] = patient
    payload['query'] = query
    return jsonify(payload)

# PUT to update patient with id, same as for passengers
@routes.route("/api/integratedML/patients/<int:id>", methods=["PUT"])
def updatePatient(id):
    query = "SELECT ID FROM Titanic_Table.Passenger WHERE ID = ?"
    rs = iris.sql.exec(query, str(id))
    try :
        rs.__next__()
    except:        
        return make_response(
            'Not Found',
            204
        )
    patient = request.get_json()
    query = "UPDATE Noshow_Table.Appointment SET gender = ?, scheduledDay = DATE(?), scheduledHour = ?, appointmentDay = DATE(?), age = ?, neighborhood = ?, scholarship = ?, hypertension = ?, diabetes = ?, alcoholism = ?, handicap = ?, smsReceived = ?, noShow = ? WHERE ID = ?"
    try:
        iris.sql.exec(query, patient['gender'], patient['scheduledDay'], patient['scheduledHour'], patient['appointmentDay'], patient['age'], patient['neighborhood'], patient['scholarship'], patient['hypertension'], patient['diabetes'], patient['alcoholism'], patient['handicap'], patient['smsReceived'], patient['noShow'], id)
    except:
        return make_response(
            'Bad Request',
            400
        )
    payload = {
        'query': query,
    }
    return jsonify(payload)

# DELETE patient with id, same as for passengers
@routes.route("/api/integratedML/patients/<int:id>", methods=["DELETE"])
def deletePatient(id):
    payload = {}
    query = "DELETE FROM Noshow_Table.Appointment WHERE ID = ?"
    try:
        iris.sql.exec(query, str(id))
    except:
        return make_response(
            'Not Found',
            204
        )
    payload['query'] = query
    return jsonify(payload)

