import MySQLdb
from MySQLdb import Error
import datetime

# Exemple d'utilisation :

# 1ère étape - instanciation :
#my_sql = Mysql(host='localhost', user='root', password='root', database='my_database')

# 2ème étape - requetage :
#my_sql.insert('user', username='test')
#my_result = my_sql.select('user', 'username = "test" ', 'id', 'username')

class Mysql(object):
    
    __instance   = None
    __host       = None
    __user       = None
    __password   = None
    __database   = None
    __session    = None
    __connection = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance or not cls.__database:
            cls.__instance = super(Mysql, cls).__new__(cls)

        return cls.__instance

    def __init__(self, host, user, password, database):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database

    def __open(self):
        try:
            conn = MySQLdb.connect(host=self.__host, user=self.__user, password=self.__password, database=self.__database)
            self.__connection = conn
            self.__session = conn.cursor()

        except Error as e:
            print(e)

    def __close(self):
        self.__session.close()
        self.__connection.close()

    def select(self, table, where=None, *args, **kwargs):
        result = None
        query = 'SELECT '
        keys = args
        values = tuple(kwargs.values())
        l = len(keys) - 1

        for i, key in enumerate(keys):
            query += ""+key+""
            if i < l:
                query += ","

        query += ' FROM %s' % table

        if where:
            query += " WHERE %s" % where

        self.__open()
        self.__session.execute(query, values)
        number_rows = self.__session.rowcount
        number_columns = len(self.__session.description)

        if number_rows >= 1 and number_columns > 1:
            result = [item for item in self.__session.fetchall()]
        else:
            result = [item[0] for item in self.__session.fetchall()]
        self.__close()

        return result
    
    def insert(self, table, **kwargs):
        values = None
        query = "INSERT INTO %s " % table

        if kwargs:
            keys = kwargs.keys()
            values = tuple(kwargs.values())
            query += "(" + ",".join(["`%s`"] * len(keys)) % tuple(keys) + ") VALUES (" + ",".join(["%s"] * len(values)) + ")"

            if table == "player":
                query += "ON DUPLICATE KEY UPDATE `id` = LAST_INSERT_ID(`id`), "
                keys   = kwargs.keys()
                values += tuple(kwargs.values())
                l = len(keys) - 1
                for i, key in enumerate(keys):
                    query += "`"+key+"` = %s"
                    if i < l:
                        query += ","

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()
        self.__close()

        return self.__session.lastrowid
