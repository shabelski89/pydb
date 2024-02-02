import os
import sys
from typing import List, Optional, Tuple

try:
    import pymysql
except ModuleNotFoundError as Error:
    print(Error)

try:
    import psycopg2
except ModuleNotFoundError as Error:
    print(Error)

try:
    import cx_Oracle
except ModuleNotFoundError as Error:
    print(Error)


class DbException(Exception):
    """
    Exception raised for errors in DataBase.
    Attributes: message - explanation of the error
    """
    def __init__(self, message):
        self.message = f"Error execute query - {message}"
        super().__init__(self.message)


class ExecutionResponse:
    """
    Class that is returned by execute() method of a DataBaseConnector class.
    :param result: Optional, return List[Dict] rows if success is True
    :param header: Optional, return List[Dict] rows headers if success is True
    :param count: Optional, return count() number of execute() results
    """

    def __init__(self,
                 result: Optional[List[Tuple[str, ...]]] = None,
                 header: Optional[Tuple[str, ...]] = None,
                 count: Optional[int] = None):
        self.result = result
        self.header = header
        self.count = count

    def __repr__(self):
        return self.result


class UniDbConnector:
    """
    Universal DataBase connector class.
    """

    def __init__(self, config: dict):
        """
        param config: Dict of params to connect DB.
        {
        "host": DB hostname or IP-address,
        "port": DB port,
        "user": DB Username,
        "password": DB password,
        "database": DB/SCHEMA name,
        "dbms": DBMS Vendor ['mysql', 'oracle', 'postgres']
        }
        """
        self.config: dict = config
        self.dbms: str = config.pop('dbms')
        self.db: str = config.pop('database')
        self.__connect = getattr(self, f"_get_connection_{self.dbms}")()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__connect.close()

    def _get_connection_postgres(self):
        """Connect to a Postgres database."""
        self.config['dbname'] = self.db
        try:
            self.__connect = psycopg2.connect(**self.config)
            self.__connect.autocommit = True
            return self.__connect
        except psycopg2.DatabaseError as Error:
            raise DbException(message=Error)

    def _get_connection_mysql(self):
        """Connect to a MySQL database."""
        self.config['db'] = self.db
        try:
            self.__connect = pymysql.connect(**self.config)
            self.__connect.autocommit = True
            return self.__connect
        except pymysql.DatabaseError as Error:
            raise DbException(message=Error)

    def _get_connection_oracle(self):
        """Connect to a Oracle database."""
        try:
            if sys.platform.startswith("linux"):
                lib_dir = os.environ.get("LD_LIBRARY_PATH")
                cx_Oracle.init_oracle_client(lib_dir=lib_dir)
            elif sys.platform.startswith("win32"):
                lib_dir = os.environ.get("ORACLE_HOME")  # WINDOWS ENV PATH NOT TESTED!
                cx_Oracle.init_oracle_client(lib_dir=lib_dir)
        except Exception as Error:
            raise DbException(message=Error)

        try:
            try:
                self.config['dsn'] = cx_Oracle.makedsn(self.config.get('host'),
                                                       self.config.get('port'),
                                                       service_name=self.db)

                self.config = dict(user=self.config['user'], password=self.config['password'], dsn=self.config['dsn'])
                self.__connect = cx_Oracle.connect(**self.config)
                self.__connect.autocommit = True
                return self.__connect
            except cx_Oracle.DatabaseError as Error:
                print(f'Service name with {self.db} not found!')

            self.config['dsn'] = cx_Oracle.makedsn(self.config.get('host'),
                                                   self.config.get('port'),
                                                   self.db)
            self.config = dict(user=self.config['user'], password=self.config['password'], dsn=self.config['dsn'])
            self.__connect = cx_Oracle.connect(**self.config)
            self.__connect.autocommit = True
            return self.__connect

        except cx_Oracle.DatabaseError as Error:
            raise DbException(message=Error)

    def execute(self, query: str, params: tuple = None):
        """
        Method to execute sql query
        :raise cx_Oracle.DatabaseError, pymysql.DatabaseError, psycopg2.DatabaseError: raised when any DB error
        """
        try:
            cursor = self.__connect.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
        except (cx_Oracle.DatabaseError, pymysql.DatabaseError, psycopg2.DatabaseError) as Error:
            raise DbException(message=Error)
        return cursor

    def fetchmany(self, query: str, params: tuple = None, size=10000) -> tuple:
        """
        Method to fetchmany data
        :param query: sql query to execute
        :param params: params in where clause
        :param size: count rows to return
        :return: yield tuple of query results
        """
        cursor = self.execute(query=query, params=params)
        while True:
            results = cursor.fetchmany(size)
            if not results:
                break
            yield results

    def fetchmany_er(self, query: str, params: tuple = None, size=10000) -> ExecutionResponse:
        """
        Special method to fetchmany ExecutionResponse instance
        :param query: sql query to execute
        :param params: params in where clause
        :param size: count rows to return
        :return: yield ExecutionResponse of query results
        """
        cursor = self.execute(query=query, params=params)
        while True:
            results = cursor.fetchmany(size)
            if not results:
                break
            header = tuple(desc[0] for desc in cursor.description)
            yield ExecutionResponse(result=results, header=header, count=cursor.rowcount)

    def fetchall(self, query: str, params: tuple = None) -> List[tuple]:
        """
        Method to fetchall data
        :param query: sql query to execute
        :param params: params in where clause
        :return: List[tuple] of query results
        """
        cursor = self.execute(query=query, params=params)
        result = [row for row in cursor.fetchall()]
        return result

    def fetchall_er(self, query: str, params: tuple = None) -> List[ExecutionResponse]:
        """
        Special method to fetchall ExecutionResponse instance
        :param query: sql query to execute
        :param params: params in where clause
        :return: List[ExecutionResponse] of query results
        """
        cursor = self.execute(query=query, params=params)
        header = tuple(desc[0] for desc in cursor.description)
        result = [ExecutionResponse(result=row, header=header, count=cursor.rowcount) for row in cursor.fetchall()]
        return result
