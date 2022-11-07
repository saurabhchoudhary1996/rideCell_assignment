from os import path, getcwd
from configparser import ConfigParser

#Folder Path
defaultPath = path.join(getcwd())
logDir = path.join(defaultPath, 'log')

#init config file
config = ConfigParser()
config.read(path.join(defaultPath,'PDconfig.ini'))

#log level
loggerLevel = int(config.get('default','loglevel'))

#order type
PAPER_BOOK = 'paper_book'
EBOOK = 'e-book'

#url
SHIPMENT_URL = config.get('default','SHIPMENT_URL')

#Shipment status
DISPATCHED = 'dispatched'
OUT_FOR_DELIVERY = 'out for delivery'
SHIPPED = 'shipped'
DELIVERED = 'delivered'