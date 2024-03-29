from database.client.utils import *
from database.database_manager import *


class ClientManager(DatabaseManager):
    def __init__(self, user, password, host, port, dbname="postgres"):
        super().__init__(user, password, host, port, dbname)
        self._connect_database()
        self._create_cursor()

    def _create_table_clients(self):
        try:
            if check_table_query(cursor=self._cursor, table_name="clients"):
                create_table_query = '''
                    CREATE TABLE IF NOT EXISTS Clients(
                    client_id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50),
                    last_name VARCHAR(50),
                    email VARCHAR(100) UNIQUE);
                '''

                self._cursor.execute(create_table_query)
                self._conn.commit()

                print("Таблица успешно создана в PostgreSQL")
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)

    def _create_table_phones(self):
        try:
            if check_table_query(cursor=self._cursor, table_name="phones"):
                create_table_query = '''
                    CREATE TABLE IF NOT EXISTS Phones (
                    phone_id SERIAL PRIMARY KEY,
                    client_id INTEGER REFERENCES Clients(client_id),
                    phone_number VARCHAR(20));
                '''

                self._cursor.execute(create_table_query)
                self._conn.commit()

                print("Таблица успешно создана в PostgreSQL")
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)

    def add_client(self, first_name, last_name, email):
        try:
            if get_user_not_exists(cursor=self._cursor, email=email):
                insert_client_query = '''
                    INSERT INTO Clients(first_name, last_name, email)
                    VALUES (%s, %s, %s) RETURNING client_id;
                '''

                self._cursor.execute(insert_client_query, (first_name, last_name, email))
                client_id = self._cursor.fetchone()[0]

                print("Клиент успешно добавлен")
                self._conn.commit()
                return client_id

            return None
        except (Exception, Error) as error:
            print("Ошибка при добавлении клиента", error)

    def add_phone_number(self, client_id, phone_number):
        try:
            if get_user_exists(self._cursor, client_id) and get_user_exists(self._cursor, client_id, phone_number):
                insert_phone_query = '''
                    INSERT INTO Phones(client_id, phone_number)
                    VALUES (%s, %s) RETURNING phone_id;
                '''
                self._cursor.execute(insert_phone_query, (client_id, phone_number))

                self._conn.commit()
                print("Телефон успешно добавлен")
        except (Exception, Error) as error:
            print("Ошибка при добавлении телефона", error)

    def update_client(self, first_name, last_name, email):
        try:
            if get_user_not_exists(self._cursor, email=email):
                update_client_query = '''
                    UPDATE Clients
                    SET first_name=%s, last_name=%s, email=%s
                    WHERE email=%s;
                '''
                self._cursor.execute(update_client_query, (first_name, last_name, email, email))

                self._conn.commit()
                print("Данные о клиенте успешно изменены")
        except (Exception, Error) as error:
            print("Ошибка при изменении данных о клиенте", error)

    def del_phone(self, client_id, phone_number):
        try:
            if get_number_exists(self._cursor, client_id, phone_number):
                delete_phone_query = '''
                    DELETE FROM Phones
                    WHERE client_id = %s AND phone_number = %s;
                    '''
                self._cursor.execute(delete_phone_query, (client_id, phone_number))

                self._conn.commit()
                print("Телефон успешно удален")
        except (Exception, Error) as error:
            print("Ошибка при удалении телефона", error)

    def del_client(self, client_id):
        try:
            if get_user_exists(self._cursor, client_id):
                delete_phones_query = '''
                    DELETE FROM Phones
                    WHERE client_id = %s;
                '''
                self._cursor.execute(delete_phones_query, (client_id,))

                delete_client_query = '''
                    DELETE FROM Clients
                    WHERE client_id = %s;
                '''
                self._cursor.execute(delete_client_query, (client_id,))

                self._conn.commit()
                print("Клиент успешно удален")
        except (Exception, Error) as error:
            print("Ошибка при удалении клиента", error)

    def find_client(self, first_name=None, last_name=None, email=None, phone_number=None):
        try:
            find_client_query = '''
                SELECT * FROM Clients
                WHERE first_name ILIKE %s
                OR last_name ILIKE %s
                OR email ILIKE %s
                OR client_id IN (SELECT client_id FROM Phones WHERE phone_number = %s);
            '''
            self._cursor.execute(find_client_query, (first_name, last_name, email, phone_number))
            clients = self._cursor.fetchall()

            if clients:
                print("Найденные клиенты:")
                for client in clients:
                    print(client)
            else:
                print("Клиенты не найдены")
        except (Exception, Error) as error:
            print("Ошибка при поиске клиента", error)

    def create_client(self, name_database):
        try:
            self._close_connection()
            conn = self._create_database(name_database)
            if conn:
                self._conn = conn
                self._create_cursor()
                print("Подключение к базе данных успешно установлено.")

            self._create_table_clients()
            self._create_table_phones()

            print("Таблицы успешно созданы")
        except (Exception, Error) as error:
            print("Ошибка при создании базы данных:", error)
