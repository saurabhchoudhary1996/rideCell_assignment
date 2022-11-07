from PDResMsg import *
from PDLogging import *
import PDdbconnection


class PDUser:
    def __init__(self) -> None:
        pass

    @addlog
    def register(self, userDetail):
        db = PDdbconnection.Database()
        try:
            # check user is already exist
            if not db.check_user_exist(userDetail['emailAddress']):
                # adding user
                result = db.add_user(userDetail)
                db.db_commit()
            else:
                result = PD_MISCELLANEOUS['PD_USER_EXIST']
            return result
        except:
            raise CustomException(PD_ERROR['PD_SIGNUP_FAILED'])
        finally:
            db.db_close()

    @addlog
    def login(self, userDetail):
        db = PDdbconnection.Database()
        try:
            # check user is already exist
            userID = db.get_userID(userDetail['emailAddress'], userDetail['password'])
            if userID:
                return userID[0]
            else:
                return PD_MISCELLANEOUS['PD_INVALID_USER']
        except:
            raise CustomException(PD_ERROR['PD_SIGNUP_FAILED'])
        finally:
            db.db_close()

