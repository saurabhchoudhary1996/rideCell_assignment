import PDdbconnection
from PDenv import database
from PDResMsg import *
from PDLogging import *

class PDBuilder():
    def __init__(self) -> None:
        pass

    @addlog
    def initDataBase(self):
        dbID = PDdbconnection.Initialize_Database()
        try:
            if (database,) not in dbID.checkIfDatabasePresent():
                PDInfo('Database is NOT present... Creating NEW database...')
                dbID.createRemoveDatabase()
                PDInfo('New database created successfully')
        except:
            raise PD_ERROR['PD_INIT_FAILED']
        finally:
            dbID.db_close()
        db = PDdbconnection.Database()
        try:
            #remove if tables exists
            #then create tables
            if db.dropTableIfExist():
                    PDInfo('Deleting log folder and create tables if not exist....')
                    if db.create_database():
                        db.add_dummy_products()
                        db.db_commit()
                        return PD_SUCCESS['PD_INIT_SUCCESSFUL']
                    else:
                        db.db_rollback()
                        return PD_ERROR['PD_INIT_FAILED']
            else:
                db.db_rollback()
                return PD_ERROR['PD_INIT_FAILED']
        except Exception as e:
            PDException(e)
            raise CustomException(PD_ERROR['PD_INIT_FAILED'])
        finally:
            db.db_close()