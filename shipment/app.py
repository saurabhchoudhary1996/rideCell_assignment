from flask import Flask, jsonify, request

#Module
import SPBuilder
from SPResMsg import *
from SPResCode import *
from SPLogging import *
from SPShipment import *

app = Flask(__name__)

#init Database
@app.route('/', methods = ["POST"])
def init():
   try:
      builderObj = SPBuilder.SPBuilder()
      result = builderObj.initDataBase()
      if result == SP_SUCCESS['SP_INIT_SUCCESSFUL']:
         response = HttpStatus.ok_200.value
      else:
         response = HttpStatus.internal_server_error_500.value
   except CustomException as ce:
        SPException(ce.getErrMsg())
        result  = ce.getErrMsg()
        response = HttpStatus.internal_server_error_500.value
   except Exception as e:
        SPException(e)
        result = SP_ERROR['SP_INIT_FAILED']
        response = HttpStatus.internal_server_error_500.value
   return jsonify(result), response


@app.route('/get-shipment-status', methods = ["POST"])
def get_shipment_status():
   try:
      userID = request.headers['user_id']
      shipmentID = request.form['shipment_id']
      result = SPShipment(shipmentID=shipmentID, userID=userID).getShipmentStatus()
      response = HttpStatus.ok_200.value
   except CustomException as ce:
        SPException(ce.getErrMsg())
        result  = ce.getErrMsg()
        response = HttpStatus.internal_server_error_500.value
   except Exception as e:
        SPException(e)
        result = SP_ERROR['SP_SHIPMENT_STATUS_FAILED']
        response = HttpStatus.internal_server_error_500.value
   return jsonify(result), response


@app.route('/create-shipment', methods = ["POST"])
def create_shipment():
   try:
      #get userID from signup and login
      userID = request.headers['user_id']
      productIDList = request.form['productList']
      orderID = request.form['order_id']
      result = SPShipment(userID=userID).createShipment(productList=productIDList, orderID=orderID)
      response = HttpStatus.ok_200.value
   except CustomException as ce:
        SPException(ce.getErrMsg())
        result  = ce.getErrMsg()
        response = HttpStatus.internal_server_error_500.value
   except Exception as e:
        SPException(e)
        result = SP_ERROR['SP_CREATE_SHIPMENT_FAILED']
        response = HttpStatus.internal_server_error_500.value
   return jsonify(result), response

if __name__ == '__main__':
   app.run(
            host='0.0.0.0',
            port=5001,
            debug=True
         )
