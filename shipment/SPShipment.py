import SPdbconnection
from SPResMsg import *
import json
from SPLogging import addlog


class SPShipment():
    
    def __init__(self, userID, shipmentID = None):
        self.__shipmentID = shipmentID
        self.__userID = userID

    @addlog
    def createShipment(self, productList, orderID):
        productList = json.loads(productList)
        db = SPdbconnection.Database()
        try:
            shipmentIDList = db.add_to_shipment(productList, orderID, self.__userID)
            db.db_commit()
            return shipmentIDList
        except:
            raise CustomException(SP_ERROR['SP_CREATE_SHIPMENT_FAILED'])
        finally:
            db.db_close() 

    @addlog
    def getShipmentStatus(self):
        db = SPdbconnection.Database(realDictCursor=True)
        try:
            shipmentStatus = db.get_shipment_status(self.__shipmentID)   
            return dict(shipmentStatus)
        except:
            raise CustomException(SP_ERROR['SP_SHIPMENT_STATUS_FAILED'])
        finally:
            db.db_close()

