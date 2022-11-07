from os import path, getcwd
from configparser import ConfigParser

#Folder Path
defaultPath = path.join(getcwd())
logDir = path.join(defaultPath, 'log')

#init config file
config = ConfigParser()
config.read(path.join(defaultPath,'SPconfig.ini'))

#log level
loggerLevel = int(config.get('default','loglevel'))

#Shipment status
DISPATCHED = 'dispatched'
OUT_FOR_DELIVERY = 'out for delivery'
SHIPPED = 'shipped'
DELIVERED = 'delivered'
