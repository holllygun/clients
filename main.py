import psycopg2
conn = psycopg2.connect(database="clients_db", user="postgres", password="...")


def create_tables(conn):
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
            client_phone VARCHAR(20)
        );
        """)
    conn.commit()
    conn.close()

    
def add_new_client(conn, name, surname, email):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client_information(name, surname, email) VALUES (%s, %s, %s);
        """, (name, surname, email))
        conn.commit()
        cur.execute("""
        SELECT * FROM client_information;
        """)
        print(cur.fetchall())
    conn.close()


def add_new_phone(conn, client_id, client_phone):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client_phone(client_id, client_phone) VALUES (%s, %s);
        """, (client_id, client_phone))
        conn.commit()
        cur.execute("""
        SELECT * FROM client_phone;
        """)
        print(cur.fetchall())
    conn.close()


def change_information(conn, id:int):
    name = input('Введите имя')
    surname = input('Введите фамилию')
    email = input('Введите e-mail')
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE client_information SET name=%s, surname=%s, email=%s WHERE id=%s;
        """, (name, surname, email, id))
        cur.execute("""
        SELECT * FROM client_information;
        """)
        print(cur.fetchall())
    conn.close()


def delete_phone(conn, id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM client_phone WHERE id = %s;
        """, (id,))
        cur.execute("""
        SELECT * FROM client_phone;
        """)
        print(cur.fetchall())
    conn.close()


def delete_client(conn, id:int):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM client_phone WHERE client_id=%s;
        """, (id,))
        cur.execute("""
        DELETE FROM client_information WHERE id=%s;
        """, (id,))
        cur.execute("""
        SELECT * FROM client_information;
        """)
        print(cur.fetchall())
        conn.close()


def find_client(conn, surname):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT id, name, surname, email FROM client_information WHERE surname = %s;
        """, (surname,))
        print(cur.fetchone())

create_tables(conn)
add_new_client(conn, 'Eugene', 'Potapov', 'Potapov123@mail.ru')
add_new_phone(conn,1, +7665231145)
add_new_phone(conn,1, +7665231349)
change_information(conn, 1)
delete_phone(conn, 2)
delete_client(conn, 1)
find_client(conn, 'Potapov')

