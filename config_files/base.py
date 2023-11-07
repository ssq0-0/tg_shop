import sqlite3


def registration_in_base(id, name, age, number, address):
    root, balance = 0, 0
    sql_connect = sqlite3.connect('shop_base.db')
    cursor = sql_connect.cursor()
    print('Подключен к базе данных')

    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        id TEXT,
        name TEXT,
        balance INT,
        age INT,
        number TEXT,
        address TEXT,
        root INT
    )""")
    sql_connect.commit()

    cursor.execute(f"SELECT id FROM users WHERE id = '{id}'")
    if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", (id, name, balance, age, number, address, root))
        sql_connect.commit()
    else:
        cursor.execute("UPDATE users SET name = ?, balance = ?,age = ?, number = ?, address = ? WHERE id = ?", (name, balance, age, number, address, id))
        sql_connect.commit()
    sql_connect.close()


def get_account_info(user_id):
    sql_connect = sqlite3.connect('shop_base.db')
    cursor = sql_connect.cursor()

    request = cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return request


def get_root(user_id):
    sql_connect = sqlite3.connect('shop_base.db')
    cursor = sql_connect.cursor()

    request = cursor.execute("SELECT root FROM users WHERE id = ?", (user_id,)).fetchone()
    return request[0]


def catalog(articul, category, price, count):
    sql_connection = sqlite3.connect('shop_base.db')
    cursor = sql_connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS catalog(
        category TEXT,
        articul TEXT,
        price INT,
        count INT
    )""")
    sql_connection.commit()

    cursor.execute(f"SELECT articul FROM  catalog WHERE articul = ?", (articul,))
    if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO catalog VALUES (?, ?, ?, ?)", (articul, category, price, count))
        sql_connection.commit()
    else:
        pass
    sql_connection.close()


def delete_product(art):
    sql_connection = sqlite3.connect('shop_base.db')
    cursor = sql_connection.cursor()
    cursor.execute("DELETE FROM catalog WHERE articul = ?", (art,))

    if cursor.rowcount > 0:
        sql_connection.commit()
        return 'deleted'
    else:
        return 'not_found'
