import PDdbconnection
from PDResMsg import *
from PDLogging import *
from PDMicroService import *
from PDSetting import EBOOK, PAPER_BOOK, DELIVERED

import json

class PDProduct():
    
    def __init__(self) -> None:
        pass

    @addlog
    def getProductList(self):
        db = PDdbconnection.Database(realDictCursor = True)
        try:
            #fetching product list
            productList = [dict(productDetail) for productDetail in db.get_product_list()]
            return productList
        except:
            raise CustomException(PD_ERROR['PD_PRODUCT_LIST_FAILED'])
        finally:
            db.db_close()

    @addlog
    def addToCart(self, cart, userID):
        cart = json.loads(cart)
        db = PDdbconnection.Database()
        try:
            #adding products to cart
            db.add_to_cart(cart, userID)
            db.db_commit()
            return PD_SUCCESS['PD_ADDED_TO_CART_SUCCESS']
        except:
            raise CustomException(PD_ERROR['PD_ADDED_TO_CART_FAILED'])
        finally:
            db.db_close()
    
    @addlog
    def getCartProductList(self, userID):
        db = PDdbconnection.Database(realDictCursor=True)
        try:
            #adding products to cart
            cartProductList = [dict(cartProduct) for cartProduct in db.get_cart_product(userID)]
            return cartProductList
        except:
            raise CustomException(PD_ERROR['PD_FETCH_CART_FAILED'])
        finally:
            db.db_close()
    
    @addlog
    def removeFromCart(self, cart, userID):
        cart = json.loads(cart)
        db = PDdbconnection.Database()
        try:
            #adding products to cart
            db.remove_from_cart(cart, userID)
            db.db_commit()
            return PD_SUCCESS['PD_REMOVE_FROM_CART_SUCCESS']
        except:
            raise CustomException(PD_ERROR['PD_REMOVED_FROM_CART_FAILED'])
        finally:
            db.db_close()

    @addlog
    def getShipmentStatus(self, productID, userID):
        db = PDdbconnection.Database()
        try:
            #adding products to cart
            orderType = db.get_orderType(productID, userID)
            if orderType == PAPER_BOOK:
                shipmentID = db.get_shipmentID(productID, userID)
                if shipmentID:
                    result = PDMicroService(userID).getShipmentStatus(shipmentID=shipmentID[0])

            elif orderType == EBOOK:
                result = DELIVERED
            return result
        except:
            raise CustomException(PD_ERROR['PD_SHIPMENT_STATUS_FAILED'])
        finally:
            db.db_close()
        
    @addlog
    def conformOrder(self, userID):
        cartProductList = self.getCartProductList(userID=userID)
        db = PDdbconnection.Database()
        try:
            #Confirm Order
            orderID = db.create_order(userID)
            shipmentProductList = [] 
            eProductList = []

            for cartProduct in cartProductList:
                if cartProduct['order_type'] == PAPER_BOOK:
                    shipmentProductList.append(cartProduct['product_id'])
                else:
                    eProductList.append(cartProduct['product_id'])
            if shipmentProductList:
                result = PDMicroService(userID).createShipment(productIDList=shipmentProductList, orderID=orderID)
            
                if result is not PD_ERROR['PD_CREATE_SHIPMENT_FAILED']:
                    for res in result:
                        productList = db.get_product_detail(res['product_id'])
                        db.add_to_purchasedProduct(productList, userID, orderID, res['shipment_id'], PAPER_BOOK)
                else:
                    return PD_ERROR['PD_CREATE_SHIPMENT_FAILED']
                    
            for eProductID in eProductList:
                productList = db.get_product_detail(eProductID)
                db.add_to_purchasedProduct(productList, userID, orderID, None, EBOOK)
            
            db.db_commit()
            return PD_SUCCESS['PD_ORDER_CONFORM_SUCCESS']
        except:
            db.db_rollback()
            raise CustomException(PD_ERROR['PD_SHIPMENT_ORDER_FAILED'])
        finally:
            db.db_close()