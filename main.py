import psycopg2
with psycopg2.connect(database="clients_db", user="postgres", password="...") as conn:
    def delete_tables():
        with conn.cursor() as cur:
            cur.execute("""
            DROP TABLE client_phone;
            DROP TABLE client_information;""")

    def create_tables():
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS client_information(
                id SERIAL PRIMARY KEY,
                name VARCHAR(40),
                surname VARCHAR(40),
                email VARCHAR(40) UNIQUE
            ); 
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS  client_phone(
                id SERIAL PRIMARY KEY,
                client_id INTEGER NOT NULL REFERENCES client_information(id),
                c_phone VARCHAR(20) UNIQUE
            );
            """)


    def add_new_client(name, surname, email):
        with conn.cursor() as cur:
            cur.execute("""
                SELECT EXISTS(SELECT email FROM client_information WHERE email = %s);
                """, (email,))
            exists = cur.fetchone()[0]
            if exists:
                print('Такой клиент уже существует')
            else:
                cur.execute("""
                INSERT INTO client_information(name, surname, email) VALUES (%s, %s, %s);
                """, (name, surname, email))

                cur.execute("""
                SELECT * FROM client_information;
                """)
                print(cur.fetchall())


    def add_new_phone(client_id, phone):
        phone = str(phone)
        with conn.cursor() as cur:
            cur.execute("""
            SELECT EXISTS(SELECT c_phone FROM client_phone WHERE c_phone=%s);
            """, (phone,))
            if_exists = cur.fetchone()[0]
            if if_exists:
                print('Такой номер уже существует')
            else:
                cur.execute("""
                INSERT INTO client_phone(client_id, c_phone) VALUES (%s, %s);
                """, (client_id, phone))
                cur.execute("""
                SELECT * FROM client_phone;
                """)
                print(cur.fetchall())


    def change_information(id:int, name=None, surname=None, email=None):
        if name is not None and surname is not None and email is not None:
            with conn.cursor() as cur:
                cur.execute("""
                UPDATE client_information SET name=%s, surname=%s, email=%s WHERE id=%s;
                """, (name, surname, email, id))
                cur.execute("""
                SELECT * FROM client_information;
                """)
                print(cur.fetchall())
        elif name is not None and surname is not None and email is None:
            with conn.cursor() as cur:
                cur.execute("""
                       UPDATE client_information SET name=%s, surname=%s WHERE id=%s;
                       """, (name, surname, id))
                cur.execute("""
                       SELECT * FROM client_information;
                       """)
                print(cur.fetchall())
        elif name is not None and surname is None and email is not None:
            with conn.cursor() as cur:
                cur.execute("""
                       UPDATE client_information SET name=%s, email=%s WHERE id=%s;
                       """, (name, email, id))
                cur.execute("""
                       SELECT * FROM client_information;
                       """)
                print(cur.fetchall())
        elif name is None and surname is not None and email is not None:
             with conn.cursor() as cur:
                cur.execute("""
                       UPDATE client_information SET surname=%s, email=%s WHERE id=%s;
                       """, (surname, email, id))
                cur.execute("""
                       SELECT * FROM client_information;
                       """)
                print(cur.fetchall())
        elif name is not None and surname is None and email is None:
            with conn.cursor() as cur:
                cur.execute("""
                       UPDATE client_information SET name=%s WHERE id=%s;
                       """, (name, id))
                cur.execute("""
                       SELECT * FROM client_information;
                       """)
                print(cur.fetchall())
        elif name is None and surname is not None and email is None:
            with conn.cursor() as cur:
                cur.execute("""
                       UPDATE client_information SET surname=%s WHERE id=%s;
                       """, (surname, id))
                cur.execute("""
                       SELECT * FROM client_information;
                       """)
                print(cur.fetchall())
        elif name is None and surname is None and email is not None:
            with conn.cursor() as cur:
                cur.execute("""
                       UPDATE client_information SET email=%s WHERE id=%s;
                       """, (email, id))
                cur.execute("""
                       SELECT * FROM client_information;
                       """)
                print(cur.fetchall())


    def delete_phone(client: int):
        with conn.cursor() as cur:
            cur.execute("""
                SELECT EXISTS(SELECT id FROM client_phone WHERE id = %s);
                """, (client,))
            if_exists = cur.fetchone()[0]
            if if_exists:
                cur.execute("""
                DELETE FROM client_phone WHERE id = %s;
                """, (client,))
                print('Номер удалён.')
            else:
                print('Такого клиента не сущетсвует')


    def delete_client(c_id:int):
        with conn.cursor() as cur:
            cur.execute("""
                SELECT EXISTS(SELECT client_id FROM client_phone WHERE client_id = %s);
                """, (c_id,))
            exists = cur.fetchone()[0]
            if exists:
                cur.execute("""
                                DELETE FROM client_phone WHERE client_id = %s;
                                """, (c_id,))

            cur.execute("""
            SELECT EXISTS(SELECT id FROM client_information WHERE id = %s);
            """, (c_id,))
            exists = cur.fetchone()[0]
            if exists:
                cur.execute("""
                DELETE FROM client_information WHERE id=%s;
                """, (c_id,))
                print ('Информация о клиенте удалена.')
            else:
                print('Такого клиента не существует.')


    def find_client(inf):
        with conn.cursor() as cur:

            cur.execute("""
            SELECT name, surname, email, c_phone FROM client_information
            JOIN client_phone on client_phone.client_id = client_information.id 
            WHERE name = %s or surname = %s or email = %s or c_phone = %s;
            """, (inf, inf, inf, inf, ))
            print(cur.fetchall())


    def show_tables():
        with conn.cursor() as cur:
            a = cur.execute(""" SELECT * FROM client_information""")
            print(cur.fetchall())
            b = cur.execute("""SELECT * FROM client_phone""")
            print(cur.fetchall())

    delete_tables()
    create_tables()
    add_new_client('Eugene', 'Potapov', 'Potapov123@mail.ru')
    add_new_client('Olga', 'Ivanova', 'Ivanova3@mail.ru')
    add_new_client('Andrey','Kiselev', 'Kiselev@gmail.com')
    add_new_phone(1, +7665231145)
    add_new_phone(2, +7665231145)
    add_new_phone(2, +7666731349)
    change_information(1, None, 'Gimme', None)
    change_information(2, 'Irina', 'Ivanova', 'ivanova@mail.ru')
    delete_phone(2)
    delete_client(3)
    find_client('Eugene')
conn.close()