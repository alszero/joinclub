import cx_Oracle
from users_manage import UsersManager

class DBconfig:
    def __init__(self, username, password, host, port, service):
        self.connection = cx_Oracle.connect(f"{username}/{password}@{host}:{port}/{service}")
        self.cursor = self.connection.cursor()
        self.users_manager = UsersManager(self)  # UsersManager 객체 생성

    def get_cursor(self):
        return self.cursor

    def exit(self):
        self.cursor.close()
        self.connection.close()