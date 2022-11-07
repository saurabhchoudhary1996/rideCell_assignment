PD_ERROR = {
    'PD_INIT_FAILED': "Unable initialize project.",
    'PD_PRODUCT_LIST_FAILED': "Unable fetch products.",
    'PD_SIGNUP_FAILED': "Unable sign-up.",
    'PD_ADDED_TO_CART_FAILED': "Unable add product(s) to cart.",
    'PD_FETCH_CART_FAILED': "Unable fetch cart.",
    'PD_REMOVED_FROM_CART_FAILED': "Unable remove product(s) from cart.",
    'PD_SHIPMENT_STATUS_FAILED': "Unable fetch shipment status.",
    'PD_SHIPMENT_ORDER_FAILED': "Unable to confirm order.",
    'PD_CREATE_SHIPMENT_FAILED': "Unable create shipment."

}

PD_SUCCESS = {
    'PD_INIT_SUCCESSFUL': "Project successfully initialized.",
    'PD_ADDED_TO_CART_SUCCESS': "Product(s) successfully added.",
    'PD_REMOVE_FROM_CART_SUCCESS': "Product(s) successfully removed.",
    'PD_ORDER_CONFORM_SUCCESS': "Order is confirmed."
}

PD_MISCELLANEOUS = {
    'PD_USER_EXIST': "User already exist.",
    'PD_INVALID_USER': "Invalid email address or password."
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