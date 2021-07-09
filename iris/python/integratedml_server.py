from flask import Flask
from flask import request
from flask import jsonify
import iris
import json

app = Flask(__name__)

@app.route('/passengers',methods=['GET'])
def getAllPassengers():
  try:
      iris.cls("Util.Loader").SetNameSpace("IRISAPP")
  except:
      pass
  
  # Get query param
  if request.args.get('currPage'):
    currPage = int(request.args.get('currPage'))
  else:
    currPage=1
  if request.args.get('pageSize'):
    pageSize = int(request.args.get('pageSize'))
  else:
    pageSize=10
  name = request.args.get('name')
  tRow = 0

  # init response
  dyna = {}
  passengers = []

  if name != None :
    myquery = "SELECT Id FROM Titanic_Table.Passenger WHERE Titanic_Table.Passenger.name %STARTSWITH ?"
    rs = iris.sql.exec(myquery,name)
    for i in rs:
        passenger = iris.ref(1)
        iris.cls("Titanic.Table.Passenger")._OpenId(i[0])._JSONExportToString(passenger)
        test = iris.cls("Titanic.Table.Passenger")._OpenId(i[0])
        tezt = 'tte'
        passengers.append(json.loads(passenger.value))
        tRow = tRow + 1
  else:
    tStartRow = pageSize * currPage
    tEndRow = tStartRow + pageSize

    myquery = "SELECT Id FROM Titanic_Table.Passenger"
    rs = iris.sql.exec(myquery)
    for i in rs:
      if (tRow<tEndRow) & (tRow>=tStartRow):
        passenger = iris.ref(1)
        iris.cls("Titanic.Table.Passenger")._OpenId(i[0])._JSONExportToString(passenger)
        passengers.append(json.loads(passenger.value))
      tRow = tRow + 1
        
  dyna['total'] = tRow
  dyna['passenger'] = passengers

  return jsonify(dyna)

@app.route('/passengers',methods=['POST'])
def createPassenger():
  dyna = {}
  try:
    iris.cls("Util.Loader").SetNameSpace("IRISAPP")
  except:
    pass
  try:
      passenger = iris.cls("Titanic.Table.Passenger")._New()
      passenger._JSONImport(request.get_data())
      passenger._Save()
      passenger.passengerId = passenger._Id()
      passenger._Save()
      dyna['passengerId'] = passenger._Id()
  except :
      pass
  return dyna
  
if __name__ == '__main__':
  app.run(host='localhost', port=8080, debug=True)