import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute(""" CREATE TABLE IF NOT EXISTS Clients(
                        client_id SERIAL PRIMARY KEY, 
                        first_name VARCHAR(80) NOT NULL,
                        last_name  VARCHAR(80) NOT NULL,
                        email     VARCHAR(80) UNIQUE NOT NULL);""")
        conn.commit()

        cur.execute(""" CREATE TABLE IF NOT EXISTS Phones(
                        phone_id   SERIAL PRIMARY KEY,
                        client_id  SERIAL REFERENCES Clients(client_id),
                        phone CHAR(20) UNIQUE
                    );""")
        conn.commit()

def add_client(conn, first_name, last_name, email, phone):
    with conn.cursor() as cur:
        cur.execute(""" INSERT INTO Clients(first_name, last_name, email)
                        VALUES (%s, %s, %s);""",
                        (first_name, last_name, email))
        conn.commit()

        cur.execute(""" INSERT INTO Phones(phone)
                        VALUES (%s);""",
                        (phone,))
        conn.commit() 

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute(""" INSERT INTO Phones(client_id, phone) 
                        VALUES (%s, %s);""",
                        (client_id, phone))
        conn.commit()

def change_client(conn, client_id, first_name, last_name, email, phone=None):
    with conn.cursor() as cur:
        cur.execute(""" UPDATE Clients
                        SET first_name=%s, last_name=%s, email=%s
                        WHERE client_id=%s""",
                        (first_name, last_name, email, client_id))
        conn.commit()  

        cur.execute(""" SELECT * FROM Clients
                        WHERE client_id=%s""",
                    (client_id,))
        conn.commit()
        
def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute(""" DELETE FROM Phones
                        WHERE phone=%s;""",
                        (phone,))
        conn.commit()

        cur.execute(""" SELECT * FROM Clients
                        WHERE client_id=%s""",
                    (client_id,))
        conn.commit()

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute(""" DELETE FROM Clients
                        WHERE client_id=%s;""",
                        (client_id,))
        conn.commit()
         

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute(""" SELECT c.first_name, c.last_name, c.email FROM Clients AS c
                        LEFT JOIN Phones AS p ON c.client_id = p.client_id
                        WHERE (c.first_name = %s OR %s IS NULL)
                        AND (c.last_name = %s OR %s IS NULL)
                        AND (c.email = %s OR %s IS NULL)
                        AND (p.phone = %s OR %s IS NULL);""",
                        (first_name, first_name, last_name, last_name, email, email, phone, phone)
                    )
        conn.commit()
         
        return print(cur.fetchall())           

with psycopg2.connect(database="clients_db", user="postgres", password="1234") as conn:
    # create_db(conn)
    # add_client(conn, 'Иван', 'Петрович', 'ivan.petrovich88@gmail.com')
    # add_client(conn, 'Алексей', 'Самсонов', 'as90@gmail.com', '32350530')
    # add_phone(conn, 1, '4232555')
    # change_client(conn, 1, 'Jack', 'Black', 'jb@gmail.com')
    # delete_phone(conn, 1, '4232555')
    # delete_client(conn, 1)
    # find_client(conn, 'Алексей')

conn.close()