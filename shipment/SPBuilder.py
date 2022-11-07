import SPdbconnection
from SPenv import database
from SPResMsg import *
from SPLogging import *

class SPBuilder():
    def __init__(self) -> None:
        pass

    @addlog
    def initDataBase(self):
        dbID = SPdbconnection.Initialize_Database()
        try:
            if (database,) not in dbID.checkIfDatabasePresent():
                SPInfo('Database is NOT present... Creating NEW database...')
                dbID.createRemoveDatabase()
                SPInfo('New database created successfully')
        except:
            raise SP_ERROR['SP_INIT_FAILED']
        finally:
            dbID.db_close()
        db = SPdbconnection.Database()
        try:
            #remove if tables exists
            #then create tables
            if db.dropTableIfExist():
                    SPInfo('Deleting log folder and create tables if not exist....')
                    if db.create_database():
                        db.db_commit()
                        return SP_SUCCESS['SP_INIT_SUCCESSFUL']
                    else:
                        db.db_rollback()
                        return SP_ERROR['SP_INIT_FAILED']
            else:
                db.db_rollback()
                return SP_ERROR['SP_INIT_FAILED']
        except Exception as e:
            SPException(e)
            raise CustomException(SP_ERROR['SP_INIT_FAILED'])
        finally:
            db.db_close()