from database.client.ClientManager import ClientManager


def main():
    user = "postgres"
    password = "ROOT"
    host = "localhost"
    port = 5432
    dbname = "test"

    cm = ClientManager(user, password, host, port, dbname)

    cm.create_client("new_database")
    client_id = cm.add_client("Иван", "Иванов", "ivan@example.com")
    cm.add_phone_number(client_id=client_id, phone_number='+55555555555')

    cm.find_client(first_name='Иван', last_name='Иванов')

    cm.update_client("Новое имя", "Новая фамилия", "ivan@example.com")

    cm.del_phone(client_id, '+55555555555')

    cm.del_client(client_id)


if __name__ == '__main__':
    main()
