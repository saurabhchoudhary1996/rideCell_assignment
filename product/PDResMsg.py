PD_ERROR = {
    'PD_INIT_FAILED': {"message":"Unable initialize project."},
    'PD_PRODUCT_LIST_FAILED': {"message":"Unable fetch products."},
    'PD_SIGNUP_FAILED': {"message":"Unable sign-up."},
    'PD_ADDED_TO_CART_FAILED': {"message":"Unable add product(s) to cart."},
    'PD_FETCH_CART_FAILED': {"message":"Unable fetch cart."},
    'PD_REMOVED_FROM_CART_FAILED': {"message":"Unable remove product(s) from cart."},
    'PD_SHIPMENT_STATUS_FAILED': {"message":"Unable fetch shipment status."},
    'PD_SHIPMENT_ORDER_FAILED': {"message":"Unable to confirm order."},
    'PD_CREATE_SHIPMENT_FAILED': {"message":"Unable create shipment."}

}

PD_SUCCESS = {
    'PD_INIT_SUCCESSFUL': {"message":"Project successfully initialized."},
    'PD_ADDED_TO_CART_SUCCESS': {"message":"Product(s) successfully added."},
    'PD_REMOVE_FROM_CART_SUCCESS': {"message":"Product(s) successfully removed."},
    'PD_ORDER_CONFORM_SUCCESS': {"message":"Order is confirmed."}
}

PD_MISCELLANEOUS = {
    'PD_USER_EXIST': {"message":"User already exist."},
    'PD_INVALID_USER': {"message":"Invalid email address or password."}
}


class CustomException(Exception):
    def __init__(self, message):
        self._message = message
        super().__init__(self._message)
    
    def getErrMsg(self, additionalMessage = None):
        if additionalMessage:
            return additionalMessage + ',' + self._message['message']
        else:
            return self._message