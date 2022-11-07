import psycopg2
import psycopg2.extras
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import random
from datetime import datetime

#Modules
from PDLogging import *
from PDSetting import PAPER_BOOK
import PDenv

class Initialize_Database:
    def __init__(self) -> None:
        self._conn = psycopg2.connect(
            host=PDenv.host, user=PDenv.user, password=PDenv.password, port=PDenv.port)
        self._conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self._cur = self._conn.cursor()

    @addlog
    def createRemoveDatabase(self):
        self._cur.execute("CREATE DATABASE %s;" % PDenv.database)

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
        self._conn = psycopg2.connect(host=PDenv.host, user=PDenv.user, password=PDenv.password,
                                      database=PDenv.database, port=PDenv.port)
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
                    CREATE TABLE IF NOT EXISTS userdetail(
					user_id UUID PRIMARY KEY DEFAULT gen_random_UUID(),
					name VARCHAR(100) NOT NULL,
					email_address VARCHAR(100) NOT NULL ,
					password VARCHAR(100) NOT NULL,
					created_on TIMESTAMP NOT NULL,
					UNIQUE(email_address)
				    );

                    CREATE TABLE IF NOT EXISTS product(
					product_id UUID PRIMARY KEY DEFAULT gen_random_UUID(),
					product_name VARCHAR(100) NOT NULL,
					product_description VARCHAR(100) NOT NULL ,
					product_price INT NOT NULL
				    );

                    CREATE TABLE IF NOT EXISTS cart(
					user_id UUID,
					product_id UUID,
                    order_type VARCHAR(50) NOT NULL,
                    UNIQUE(product_id),
                    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES userdetail(user_id) on delete cascade,
                    CONSTRAINT fk_product FOREIGN KEY(product_id) REFERENCES product(product_id) on delete cascade
				    );

                    CREATE TABLE IF NOT EXISTS purchase_order(
					order_id UUID PRIMARY KEY DEFAULT gen_random_UUID(),
					user_id UUID,
                    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES userdetail(user_id) on delete cascade
                    );

                    CREATE TABLE IF NOT EXISTS purchased_product(
					user_id UUID NOT NULL,
					product_id UUID NOT NULL,
                    product_name VARCHAR(100) NOT NULL,
                    order_id UUID NOT NULL,
                    shipment_id UUID,
                    description VARCHAR(100) NOT NULL,
					price VARCHAR(50) NOT NULL,
					order_type VARCHAR(50) NOT NULL,
                    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES userdetail(user_id) on delete cascade,
                    CONSTRAINT fk_order FOREIGN KEY(order_id) REFERENCES purchase_order(order_id) on delete cascade
                    );

                ''' 
            self._cur.execute(sql)
            PDQueryCompleted(sys._getframe().f_code.co_name)
            return True
        except Exception as e:
            PDError('Unable to create database tables...')
            PDException(e)
            raise


    @addlog
    def dropTableIfExist(self):
        try:
            sql = '''
					DROP TABLE IF EXISTS userdetail CASCADE;
					DROP TABLE IF EXISTS product CASCADE;
					DROP TABLE IF EXISTS cart CASCADE;
					DROP TABLE IF EXISTS purchase_order CASCADE;
					DROP TABLE IF EXISTS purchased_product CASCADE;
				  '''
            self._cur.execute(sql)
            PDQueryCompleted(sys._getframe().f_code.co_name)
            return True
        except Exception as e:
            PDError('Unable to create database tables...')
            PDException(e)
            raise

    @addlog
    def add_dummy_products(self):
        try:
            sql = f'''
					INSERT INTO product(product_name, product_description, product_price) VALUES('Book_{random.randint(0,9)}', 'NO description available', {random.randint(500,1000)});
                    INSERT INTO product(product_name, product_description, product_price) VALUES('Book_{random.randint(0,9)}', 'NO description available', {random.randint(500,1000)});
                    INSERT INTO product(product_name, product_description, product_price) VALUES('Book_{random.randint(0,9)}', 'NO description available', {random.randint(500,1000)});
                    INSERT INTO product(product_name, product_description, product_price) VALUES('Book_{random.randint(0,9)}', 'NO description available', {random.randint(500,1000)});
                    INSERT INTO product(product_name, product_description, product_price) VALUES('Book_{random.randint(0,9)}', 'NO description available', {random.randint(500,1000)});
                    INSERT INTO product(product_name, product_description, product_price) VALUES('Book_{random.randint(0,9)}', 'NO description available', {random.randint(500,1000)});
                    INSERT INTO product(product_name, product_description, product_price) VALUES('Book_{random.randint(0,9)}', 'NO description available', {random.randint(500,1000)});
                    INSERT INTO product(product_name, product_description, product_price) VALUES('Book_{random.randint(0,9)}', 'NO description available', {random.randint(500,1000)});
                    INSERT INTO product(product_name, product_description, product_price) VALUES('Book_{random.randint(0,9)}', 'NO description available', {random.randint(500,1000)});
                    INSERT INTO product(product_name, product_description, product_price) VALUES('Book_{random.randint(0,9)}', 'NO description available', {random.randint(500,1000)});
				  '''
            self._cur.execute(sql)
            PDQueryCompleted(sys._getframe().f_code.co_name)
            return True
        except Exception as e:
            PDException(e)
            raise

    @addlog
    def add_user(self, userDetail):
        dateTime = datetime.now()
        try:
            sql = '''
					INSERT INTO userdetail(name, email_address, password, created_on) VALUES(%s, %s, %s, %s) RETURNING user_id ;
				  '''
            self._cur.execute(sql,[userDetail['name'], userDetail['emailAddress'], userDetail['password'], dateTime])
            info = self._cur.fetchone()[0]
            PDQueryCompleted(sys._getframe().f_code.co_name)
            return info
        except Exception as e:
            PDException(e)
            raise

    @addlog
    def add_to_cart(self, cartList, userID):
        try:
            for cart in cartList:
                sql = '''
                        INSERT INTO cart(product_id, order_type, user_id) VALUES(%s, %s, %s) ON CONFLICT DO NOTHING;
                    '''
                self._cur.execute(sql,[cart['product_id'], cart['order_type'], userID])
            PDQueryCompleted(sys._getframe().f_code.co_name)
        except Exception as e:
            PDException(e)
            raise

    @addlog
    def add_to_purchasedProduct(self, productDetail, userID, orderID, shipmentID, orderType):
        try:
            sql = '''
                    INSERT INTO purchased_product(user_id, product_id, product_name,order_id, shipment_id, description, price, order_type) VALUES(%s, %s, %s,%s, %s, %s,%s, %s);
                '''
            self._cur.execute(sql,[userID, productDetail[0], productDetail[1], orderID, shipmentID, productDetail[2], productDetail[3], orderType])
            PDQueryCompleted(sys._getframe().f_code.co_name)
        except Exception as e:
            PDException(e)
            raise

    @addlog
    def create_order(self, userID):
        try:
            sql = '''
                    INSERT INTO purchase_order(user_id) VALUES(%s) RETURNING order_id;
                '''
            self._cur.execute(sql,[userID])
            info = self._cur.fetchone()[0]
            PDQueryCompleted(sys._getframe().f_code.co_name)
            return info
        except Exception as e:
            PDException(e)
            raise

    @addlog
    def get_cart_product(self, userID):
        try:
            sql = '''
                    SELECT product_id, order_type FROM cart WHERE user_id = %s;
                    '''
            self._cur.execute(sql,[userID])
            info = self._cur.fetchall()
            PDQueryCompleted(sys._getframe().f_code.co_name)
            return info
        except Exception as e:
            PDException(e)
            raise

    @addlog
    def get_product_detail(self, productID):
        try:
            sql = '''
                    SELECT product_id, product_name, product_description, product_price FROM product WHERE product_id = %s;
                    '''
            self._cur.execute(sql,[productID])
            info = self._cur.fetchone()
            PDQueryCompleted(sys._getframe().f_code.co_name)
            return info
        except Exception as e:
            PDException(e)
            raise

    @addlog
    def remove_from_cart(self, cartList, userID):
        try:
            for cart in cartList:
                sql = '''
                            DELETE FROM cart WHERE user_id = %s AND product_id = %s;
                        '''
                self._cur.execute(sql,[userID, cart['product_id']])
            PDQueryCompleted(sys._getframe().f_code.co_name)
        except Exception as e:
            PDException(e)
            raise

    @addlog
    def remove_all_product_from_cart(self, userID):
        try:
            sql = '''
                        DELETE FROM cart WHERE user_id = %s;
                    '''
            self._cur.execute(sql,[userID])
            PDQueryCompleted(sys._getframe().f_code.co_name)
        except Exception as e:
            PDException(e)
            raise

    @addlog
    def get_product_list(self):
        try:
            sql = '''
					SELECT product_id, product_name, product_description, product_price FROM product;
				  '''
            self._cur.execute(sql)
            info = self._cur.fetchall()
            PDQueryCompleted(sys._getframe().f_code.co_name)
            return info
        except Exception as e:
            PDException(e)
            raise

    @addlog
    def check_user_exist(self, emailAddress):
        try:
            sql = '''
					SELECT user_id FROM userdetail WHERE email_address = %s;
				  '''
            self._cur.execute(sql, [emailAddress])
            info = self._cur.fetchone()
            PDQueryCompleted(sys._getframe().f_code.co_name)
            return info
        except Exception as e:
            PDException(e)
            raise

    @addlog
    def get_userID(self, emailAddress, password):
        try:
            sql = '''
					SELECT user_id FROM userdetail WHERE email_address = %s AND password = %s;
				  '''
            self._cur.execute(sql, [emailAddress, password])
            info = self._cur.fetchone()
            PDQueryCompleted(sys._getframe().f_code.co_name)
            return info
        except Exception as e:
            PDException(e)
            raise

    @addlog
    def get_shipmentID(self, productID, userID):
        try:
            sql = '''
					SELECT shipment_id FROM purchased_product WHERE product_id = %s AND user_id = %s;
				  '''
            self._cur.execute(sql, [productID, userID])
            info = self._cur.fetchone()
            PDQueryCompleted(sys._getframe().f_code.co_name)
            return info
        except Exception as e:
            PDException(e)
            raise

    @addlog
    def get_orderType(self, productID, userID):
        try:
            sql = '''
					SELECT order_type FROM purchased_product WHERE product_id = %s AND user_id = %s;
				  '''
            self._cur.execute(sql, [productID, userID])
            info = self._cur.fetchone()[0]
            PDQueryCompleted(sys._getframe().f_code.co_name)
            return info
        except Exception as e:
            PDException(e)
            raise

