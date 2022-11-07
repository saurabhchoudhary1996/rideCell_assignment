import psycopg2
import psycopg2.extras
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime

#Modules
from SPSetting import *
from SPLogging import *
import SPenv

class Initialize_Database:
    def __init__(self) -> None:
        self._conn = psycopg2.connect(
            host=SPenv.host, user=SPenv.user, password=SPenv.password, port=SPenv.port)
        self._conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self._cur = self._conn.cursor()

    @addlog
    def createRemoveDatabase(self):
        self._cur.execute("CREATE DATABASE %s;" % SPenv.database)

    @addlog
    def checkIfDatabasePresent(self):
        sql = 'SELECT datname FROM pg_database;'
        self._cur.execute(sql)
        info = self._cur.fetchall()
        return info

    @addlog
    def db_close(self):
        if self._cur is not None:
            self._cur.close()
        self._cur = None
        
        if self._conn is not None:
            self._conn.close()
        self._conn = None

class Database:
    #init connection and cursor
    def __init__(self, realDictCursor=False):
        self._conn = psycopg2.connect(host=SPenv.host, user=SPenv.user, password=SPenv.password,
                                      database=SPenv.database, port=SPenv.port)
        if realDictCursor:
            self._cur = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        else:
            self._cur = self._conn.cursor()

    #commit
    @addlog
    def db_commit(self):
        self._conn.commit()

    #close database
    @addlog
    def db_close(self):
        if self._cur is not None:
            self._cur.close()
        self._cur = None
        
        if self._conn is not None:
            self._conn.close()
        self._conn = None

    #rollback
    @addlog
    def db_rollback(self):
        self._conn.rollback()    
    
    #Create Tables
    @addlog
    def create_database(self):
        try:

            # You can use purchased_product to show history of user purchased items and if all items are delivered order status from order table will be delivered otherwise InProgress
            #  
            sql = '''
                    CREATE TABLE IF NOT EXISTS shipment(
                    shipment_id UUID PRIMARY KEY DEFAULT gen_random_UUID(),
                    product_id VARCHAR(100) NOT NULL,
					user_id UUID NOT NULL,
					order_id UUID NOT NULL,
					shipment_status VARCHAR(100) NOT NULL
					);
                ''' 
            self._cur.execute(sql)
            SPQueryCompleted(sys._getframe().f_code.co_name)
            return True
        except Exception as e:
            SPError('Unable to create database tables...')
            SPException(e)
            raise


    @addlog
    def dropTableIfExist(self):
        try:
            sql = '''
					DROP TABLE IF EXISTS shipment CASCADE;
				  '''
            self._cur.execute(sql)
            SPQueryCompleted(sys._getframe().f_code.co_name)
            return True
        except Exception as e:
            SPError('Unable to create database tables...')
            SPException(e)
            raise

    @addlog
    def add_to_shipment(self, productList, orderID, userID):
        try:
            shipmentIDList = []
            for productID in productList:
                SPDebug(f'productID/productID - {productID}, {userID}, {orderID}, {DISPATCHED}')
                sql = '''
                        INSERT INTO shipment(product_id, user_id, order_id, shipment_status) VALUES(%s, %s, %s, %s) ON CONFLICT DO NOTHING RETURNING shipment_id;
                    '''
                self._cur.execute(sql,[productID, userID, orderID, DISPATCHED])
                shipmentID = self._cur.fetchone()
                if shipmentID:
                    shipmentIDList.append({'product_id':productID,'shipment_id':shipmentID[0]})
            SPQueryCompleted(sys._getframe().f_code.co_name)
            return shipmentIDList
        except Exception as e:
            SPException(e)
            raise

    @addlog
    def remove_specific_shipment(self, shipmentList, userID):
        try:
            for shipmentID in shipmentList:
                sql = '''
                            DELETE FROM shipment WHERE user_id = %s AND shipment_id = %s;
                        '''
                self._cur.execute(sql,[userID, shipmentID])
            SPQueryCompleted(sys._getframe().f_code.co_name)
        except Exception as e:
            SPException(e)
            raise

    @addlog
    def remove_all_user_shipment(self, userID):
        try:
            sql = '''
                        DELETE FROM shipment WHERE user_id = %s;
                    '''
            self._cur.execute(sql,[userID])
            SPQueryCompleted(sys._getframe().f_code.co_name)
        except Exception as e:
            SPException(e)
            raise

    @addlog
    def get_shipment_list(self, userID):
        try:
            sql = '''
					SELECT shipment_id, product_id, FROM shipment WHERE user_id = %s;
				  '''
            self._cur.execute(sql, [userID])
            info = self._cur.fetchall()
            SPQueryCompleted(sys._getframe().f_code.co_name)
            return info
        except Exception as e:
            SPException(e)
            raise

    @addlog
    def get_shipment_status(self, shipment_id):
        try:
            sql = '''
					SELECT shipment_status FROM shipment WHERE shipment_id = %s;
				  '''
            self._cur.execute(sql, [shipment_id])
            info = self._cur.fetchone()
            SPQueryCompleted(sys._getframe().f_code.co_name)
            return info
        except Exception as e:
            SPException(e)
            raise

