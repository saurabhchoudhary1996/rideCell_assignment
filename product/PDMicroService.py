
import requests
from os.path import join
import json
#
from PDSetting import SHIPMENT_URL
from PDResMsg import *
from PDLogging import *

class PDMicroService():
    def __init__(self, userID) -> None:
        self.__userID = userID

    @addlog
    def getShipmentStatus(self, shipmentID):
        resp = requests.post(join(SHIPMENT_URL, "get-shipment-status"), data = {'shipment_id':shipmentID}, headers={'user_id':self.__userID})
        if resp.status_code == 200:
            return resp.text
        else:
            return PD_ERROR['PD_SHIPMENT_STATUS_FAILED']

    @addlog
    def createShipment(self, productIDList, orderID):
        resp = requests.post(join(SHIPMENT_URL, "create-shipment"), data = {'productList':json.dumps(productIDList), 'order_id':orderID}, headers={'user_id':self.__userID})
        if resp.status_code == 200:
            return resp.json()
        else:
            return PD_ERROR['PD_CREATE_SHIPMENT_FAILED']