import logging, os, PDSetting
from logging.handlers import RotatingFileHandler
from datetime import datetime
from functools import wraps

# CRITICAL = 50
# ERROR = 40
# WARNING = 30
# INFO = 20
# DEBUG = 10
# NOTSET = 0

if not os.path.exists(PDSetting.logDir):
    os.makedirs(PDSetting.logDir)

handler = RotatingFileHandler(filename=os.path.join(PDSetting.logDir,f"PD-{datetime.now().strftime('%Y-%m-%d %H_%M_%S')}.log"),mode='a', maxBytes=1024 * 1024 * 3, encoding=None,delay=False,backupCount=100)
formatter = logging.Formatter('%(asctime)s - %(thread)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(PDSetting.loggerLevel)
logger.addHandler(handler)


def PDInfo(message):
    logger.info(message)

def PDError(message):
    logger.error(message)

def PDWarn(message):
    logger.warning(message)

def PDDebug(message):
    logger.debug(message)

def PDCritical(message):
    logger.critical(message)

def PDException(message):
    logger.exception(message)

def PDStartFunc(message):
    logger.info(f'+++ {message}')

def PDEndFunc(message):
    logger.info(f'--- {message}')

def PDQueryCompleted(message):
    logger.info(f'{message} query is executed successfully')

def PDQueryRollback(message):
    logger.error(f'All queries related to {message} are rolled back')
    
def PDQueryCommitted(message):
    logger.info(f'All queries related to {message} are committed successfully')




def addlog(func):
    @wraps(func)
    def log(*args, **kwargs):
        PDInfo(f'+++ {func.__name__}')
        result =  func(*args, **kwargs)
        PDInfo(f'--- {func.__name__}')
        return result
    return log