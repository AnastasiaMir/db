import sys
from sys import stderr

from PyQt6.QtWidgets import QApplication
from PyQt6.QtSql import QSqlDatabase
import settings as st


class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        db = QSqlDatabase.addDatabase('QPSQL')
        db.setHostName(st.db_params['host'])
        db.setPort(st.db_params['port'])
        db.setUserName(st.db_params['user'])
        db.setDatabaseName(st.db_params['dbname'])
        db.setPassword(st.db_params['password'])
        ok = db.open()
        if ok:
            print('Connected to database', file=sys.stderr)
        else:
            print(f'Connection failed {db.lastError().text()}', file=stderr)
