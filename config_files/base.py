import sqlite3


def registration_in_base(id, name, age, number, address):
    sql_connect = sqlite3.connect('shops_base.db')
    cursor = sql_connect.cursor()
    print('Подключен к базе данных')

    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        id TEXT,
        name TEXT,
        age INT,
        number TEXT,
        address TEXT
    )""")
    sql_connect.commit()

    cursor.execute(f"SELECT id FROM users WHERE id = '{id}'")
    if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?)", (id, name, age, number, address))
        sql_connect.commit()
    else:
        cursor.execute("UPDATE users SET name = ?, age = ?, number = ?, address = ? WHERE id = ?", (name, age, number, address, id))
        sql_connect.commit()
    sql_connect.close()


def get_account_info(user_id):
    sql_connect = sqlite3.connect('shops_base.db')
    cursor = sql_connect.cursor()

    request = cursor.execute("SELECT * from users where id = ?", (user_id,)).fetchone()
    return request


