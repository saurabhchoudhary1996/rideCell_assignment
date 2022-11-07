import SPdbconnection
from SPResMsg import *
import json
from SPLogging import addlog
from SPSetting import *
import uuid

class SPShipment():
    
    def __init__(self, userID, shipmentID = None):
        self.__shipmentID = shipmentID
        self.__userID = userID

    @addlog
    def createShipment(self, productList, orderID):
        productList = json.loads(productList)
        db = SPdbconnection.Database()
        try:
            shipmentList = []
            for productID in productList:
                shipmentID = str(uuid.uuid4())
                db.add_to_shipment(productID, shipmentID, orderID, self.__userID)
                shipmentList.append({'product_id':productID,'shipment_id':shipmentID})
            db.db_commit()
            return json.dumps(shipmentList)
        except:
            raise CustomException(SP_ERROR['SP_CREATE_SHIPMENT_FAILED'])
        finally:
            db.db_close() 

    @addlog
    def getShipmentStatus(self):
        #shipment API code will be here
        return DISPATCHED

