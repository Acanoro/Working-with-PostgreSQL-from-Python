from psycopg2 import Error


def check_table_query(cursor, table_name):
    check_table_query = '''
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = LOWER(%s)
        );
    '''

    cursor.execute(check_table_query, (table_name,))

    if cursor.fetchone()[0]:
        print("Таблица уже существует в PostgreSQL")
        return False

    return True


def fetch_client(cursor, client_id=None, email=None):
    try:
        if client_id is not None:
            check_query = '''
                SELECT client_id
                FROM Clients
                WHERE client_id = %s;
            '''
            cursor.execute(check_query, (client_id,))
        elif email is not None:
            check_query = '''
                SELECT client_id
                FROM Clients
                WHERE email = %s;
            '''
            cursor.execute(check_query, (email,))

        return cursor.fetchone()

    except (Exception, Error) as error:
        print("Ошибка при выполнении запроса:", error)
        return None


def get_user_exists(cursor, client_id=None, email=None):
    ccq = fetch_client(cursor, client_id, email)

    if ccq:
        return True
    else:
        if client_id:
            print("Пользователя с ID", client_id, "не существует")
        elif email:
            print("Пользователь с электронной почтой", email, "не существует")

        return False


def get_user_not_exists(cursor, client_id=None, email=None):
    ccq = fetch_client(cursor, client_id, email)

    if ccq:
        if client_id:
            print("Пользователя с ID", client_id, "существует")
        elif email:
            print("Пользователь с электронной почтой", email, "существует")

        return False
    else:
        return True


def fetch_phone(cursor, client_id=None, phone_number=None):
    try:
        check_phone_query = '''
            SELECT phone_number
            FROM Phones
            WHERE phone_number = %s AND client_id = %s;
        '''
        cursor.execute(check_phone_query, (phone_number, client_id,))

        return cursor.fetchone()

    except (Exception, Error) as error:
        print("Ошибка при выполнении запроса:", error)
        return None


def get_number_exists(cursor, client_id=None, phone_number=None):
    ccq = fetch_phone(cursor, client_id, phone_number)

    if ccq:
        return True
    else:
        print("Номер уже существует")

        return False


def get_number_not_exists(cursor, client_id=None, phone_number=None):
    ccq = fetch_phone(cursor, client_id, phone_number)

    if ccq:
        print("Номер не существует")

        return False
    else:
        return True
