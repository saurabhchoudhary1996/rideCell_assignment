from flask import Flask, jsonify, request
import PDBuilder as PDBuilder
from PDUser import *
from PDProduct import *
from PDResMsg import *
from PDLogging import *
from PDResCode import HttpStatus

app = Flask(__name__)

#init Database
@app.route('/', methods = ["POST"])
def init():
   try:
      builderObj = PDBuilder.PDBuilder()
      result = builderObj.initDataBase()
      if result == PD_SUCCESS['PD_INIT_SUCCESSFUL']:
         response = HttpStatus.ok_200.value
      else:
         response = HttpStatus.internal_server_error_500.value
   except CustomException as ce:
        PDException(ce.getErrMsg())
        result  = ce.getErrMsg()
        response = HttpStatus.internal_server_error_500.value
   except Exception as e:
        PDException(e)
        result = PD_ERROR['PD_INIT_FAILED']
        response = HttpStatus.internal_server_error_500.value
   return jsonify(result), response


@app.route('/signup', methods = ["POST"])
def signup():
   try:
      userDetail = {
         'name' : request.form['name'],
         'emailAddress': request.form['email_address'],
         'password' : request.form['password']
      } 
      result = PDUser().register(userDetail)
      if result == PD_MISCELLANEOUS['PD_USER_EXIST']:
         response = HttpStatus.conflict_409.value
      else:
         response = HttpStatus.ok_200.value
   except CustomException as ce:
        PDException(ce.getErrMsg())
        result  = ce.getErrMsg()
        response = HttpStatus.internal_server_error_500.value
   except Exception as e:
        PDException(e)
        result = PD_ERROR['PD_SIGNUP_FAILED']
        response = HttpStatus.internal_server_error_500.value
   return jsonify(result), response


@app.route('/login', methods = ["POST"])
def login():
   try:
      userDetail = {
         'emailAddress': request.form['email_address'],
         'password' : request.form['password']
      } 
      result = PDUser().login(userDetail)
      if result == PD_MISCELLANEOUS['PD_INVALID_USER']:
         response = HttpStatus.conflict_409.value
      else:
         response = HttpStatus.ok_200.value
   except CustomException as ce:
        PDException(ce.getErrMsg())
        result  = ce.getErrMsg()
        response = HttpStatus.internal_server_error_500.value
   except Exception as e:
        PDException(e)
        result = PD_ERROR['PD_SIGNUP_FAILED']
        response = HttpStatus.internal_server_error_500.value
   return jsonify(result), response


@app.route('/get-product-list', methods = ["POST"])
def get_product_list():
   try:
      result = PDProduct().getProductList()
      response = HttpStatus.ok_200.value
   except CustomException as ce:
        PDException(ce.getErrMsg())
        result  = ce.getErrMsg()
        response = HttpStatus.internal_server_error_500.value
   except Exception as e:
        PDException(e)
        result = PD_ERROR['PD_PRODUCT_LIST_FAILED']
        response = HttpStatus.internal_server_error_500.value
   return jsonify(result), response


@app.route('/add-to-cart', methods = ["POST"])
def add_to_cart():
   try:
      #get userID from signup and login
      userID = request.headers['user_id']
      # cart = [{"product_id": "56409cad-6339-4996-a87a-0b51b678a539", "order_type": "e-book"}, {"product_id": "8d0d05e8-8440-49fb-9848-e72b4d9e6aca", "order_type": "paper_book"}, {"product_id": "b9eefc0d-513d-4b81-820f-3dcddb04dbbf", "order_type": "e-book"}, {"product_id": "45cce1d3-0e70-4c9a-9a15-014c1dc8f9d9", "order_type": "paper_book"}]
      cart = request.form['cart']
      result = PDProduct().addToCart(cart, userID)
      response = HttpStatus.ok_200.value
   except CustomException as ce:
        PDException(ce.getErrMsg())
        result  = ce.getErrMsg()
        response = HttpStatus.internal_server_error_500.value
   except Exception as e:
        PDException(e)
        result = PD_ERROR['PD_ADDED_TO_CART_FAILED']
        response = HttpStatus.internal_server_error_500.value
   return jsonify(result), response

@app.route('/get-cart-item', methods = ["POST"])
def get_cart_item():
   try:
      userID = request.headers['user_id']
      result = PDProduct().getCartProductList(userID)
      response = HttpStatus.ok_200.value
   except CustomException as ce:
        PDException(ce.getErrMsg())
        result  = ce.getErrMsg()
        response = HttpStatus.internal_server_error_500.value
   except Exception as e:
        PDException(e)
        result = PD_ERROR['PD_FETCH_CART_FAILED']
        response = HttpStatus.internal_server_error_500.value
   return jsonify(result), response

@app.route('/remove-from-cart', methods = ["POST"])
def remove_from_cart():
   try:
      #get userID from signup and login
      userID = request.headers['user_id']
      # cart = [{"product_id": "56409cad-6339-4996-a87a-0b51b678a539", "order_type": "e-book"}, {"product_id": "8d0d05e8-8440-49fb-9848-e72b4d9e6aca", "order_type": "paper_book"}, {"product_id": "b9eefc0d-513d-4b81-820f-3dcddb04dbbf", "order_type": "e-book"}, {"product_id": "45cce1d3-0e70-4c9a-9a15-014c1dc8f9d9", "order_type": "paper_book"}]
      cart = request.form['cart']
      result = PDProduct().removeFromCart(cart, userID)
      response = HttpStatus.ok_200.value
   except CustomException as ce:
        PDException(ce.getErrMsg())
        result  = ce.getErrMsg()
        response = HttpStatus.internal_server_error_500.value
   except Exception as e:
        PDException(e)
        result = PD_ERROR['PD_REMOVED_FROM_CART_FAILED']
        response = HttpStatus.internal_server_error_500.value
   return jsonify(result), response

@app.route('/get-shipment-status', methods = ["POST"])
def get_shipment_status():
   try:
      #get userID from signup and login
      userID = request.headers['user_id']
      productID = request.form['product_id']
      result = PDProduct().getShipmentStatus(productID, userID)
      if result == PD_ERROR['PD_SHIPMENT_STATUS_FAILED']:
         response = HttpStatus.internal_server_error_500.value
      else:
         response = HttpStatus.ok_200.value
   except CustomException as ce:
        PDException(ce.getErrMsg())
        result  = ce.getErrMsg()
        response = HttpStatus.internal_server_error_500.value
   except Exception as e:
        PDException(e)
        result = PD_ERROR['PD_SHIPMENT_STATUS_FAILED']
        response = HttpStatus.internal_server_error_500.value
   return jsonify(result), response


@app.route('/confirm-order', methods = ["POST"])
def conform_order():
   try:
      #get userID from signup and login
      userID = request.headers['user_id']
      result = PDProduct().conformOrder(userID)
      if result == PD_ERROR['PD_CREATE_SHIPMENT_FAILED']:
         response = HttpStatus.internal_server_error_500.value    
      else:
         response = HttpStatus.ok_200.value
   except CustomException as ce:
        PDException(ce.getErrMsg())
        result  = ce.getErrMsg()
        response = HttpStatus.internal_server_error_500.value
   except Exception as e:
        PDException(e)
        result = PD_ERROR['PD_REMOVED_FROM_CART_FAILED']
        response = HttpStatus.internal_server_error_500.value
   return jsonify(result), response



if __name__ == '__main__':
   app.run(
            host='0.0.0.0',
            port=5000,
            debug=True
         )
