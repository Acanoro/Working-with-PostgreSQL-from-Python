import psycopg2
from psycopg2 import Error


class DatabaseManager:
    def __init__(self, user, password, host, port, dbname="postgres"):
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._dbname = dbname

    def _connect_database(self):
        try:
            conn = psycopg2.connect(
                dbname=self._dbname,
                user=self._user,
                password=self._password,
                host=self._host,
                port=self._port
            )
            self._conn = conn
        except Error as e:
            print("Ошибка при подключении к PostgreSQL:", e)
            return None

    def _create_cursor(self):
        self._cursor = self._conn.cursor()

    def _close_connection(self):
        if self._cursor is not None:
            self._cursor.close()
        if self._conn is not None:
            self._conn.close()
            print("Соединение с PostgreSQL закрыто")

    def _create_database(self, database_name):
        try:
            self._conn = psycopg2.connect(
                dbname="postgres",
                user=self._user,
                password=self._password,
                host=self._host,
                port=self._port
            )
            self._conn.autocommit = True
            self._cursor = self._conn.cursor()

            self._cursor.execute(f"""CREATE DATABASE {database_name}""")
            print("База данных успешно создана.")
            return self._conn
        except psycopg2.errors.DuplicateDatabase:
            print("База данных уже существует.")
        except Exception as e:
            print("Ошибка при создании базы данных:", e)

    def __del__(self):
        self._close_connection()
