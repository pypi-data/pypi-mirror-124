import pymssql
from dbms.dbms_abs import DBMS

class MSSQLDB(DBMS):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._con = pymssql.connect(host=self.host, user=self.user, password=self.pwd, port=kwargs['port'], database=self.db)
        self._cursor = self._con.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.close()

    def connection(self):
        return self._con

    def cursor(self):
        return self._cursor

    def execute(self, sql, params):
        pass

    def query(self, sql, params):
        pass

    def fetchone(self):
        pass

    def fetchall(self):
        pass

    def commit(self):
        pass

    def close(self):
        pass
