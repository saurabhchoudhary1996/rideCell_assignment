import logging, os, SPSetting
from logging.handlers import RotatingFileHandler
from datetime import datetime
from functools import wraps

# CRITICAL = 50
# ERROR = 40
# WARNING = 30
# INFO = 20
# DEBUG = 10
# NOTSET = 0

if not os.path.exists(SPSetting.logDir):
    os.makedirs(SPSetting.logDir)

handler = RotatingFileHandler(filename=os.path.join(SPSetting.logDir,f"SP-{datetime.now().strftime('%Y-%m-%d %H_%M_%S')}.log"),mode='a', maxBytes=1024 * 1024 * 3, encoding=None,delay=False,backupCount=100)
formatter = logging.Formatter('%(asctime)s - %(thread)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(SPSetting.loggerLevel)
logger.addHandler(handler)


def SPInfo(message):
    logger.info(message)

def SPError(message):
    logger.error(message)

def SPWarn(message):
    logger.warning(message)

def SPDebug(message):
    logger.debug(message)

def SPCritical(message):
    logger.critical(message)

def SPException(message):
    logger.exception(message)

def SPStartFunc(message):
    logger.info(f'+++ {message}')

def SPEndFunc(message):
    logger.info(f'--- {message}')

def SPQueryCompleted(message):
    logger.info(f'{message} query is executed successfully')

def SPQueryRollback(message):
    logger.error(f'All queries related to {message} are rolled back')
    
def SPQueryCommitted(message):
    logger.info(f'All queries related to {message} are committed successfully')




def addlog(func):
    @wraps(func)
    def log(*args, **kwargs):
        SPInfo(f'+++ {func.__name__}')
        result =  func(*args, **kwargs)
        SPInfo(f'--- {func.__name__}')
        return result
    return log