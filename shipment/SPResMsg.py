SP_ERROR = {
    'SP_INIT_FAILED': "Unable initialize project.",
    'SP_CREATE_SHIPMENT_FAILED': "Unable fetch shipment status.",
    'SP_SHIPMENT_STATUS_FAILED': "Unable create shipment."
}

SP_SUCCESS = {
    'SP_INIT_SUCCESSFUL': "Project successfully initialized."
    }

SP_MISCELLANEOUS = {

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