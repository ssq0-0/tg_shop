import sqlite3


def registration_in_base(id, name, age, number, address):
    root, balance = 0, 100
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


def catalog(articul, category, price, count, name, url):
    sql_connection = sqlite3.connect('shop_base.db')
    cursor = sql_connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS catalog(
        category TEXT,
        name TEXT,
        articul TEXT,
        price INT,
        count INT
        url TEXT
    )""")
    sql_connection.commit()

    info = cursor.execute(f"SELECT articul FROM  catalog WHERE articul = ?", (articul,)).fetchall()
    if len(info) == 0:
        cursor.execute(f"INSERT INTO catalog VALUES (?, ?, ?, ?, ?, ?)", (category, name, articul,  price, count, url))
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


def send_product_from_catalog(category):
    sql_connection = sqlite3.connect('shop_base.db')
    cursor = sql_connection.cursor()

    data = cursor.execute("SELECT * FROM catalog WHERE category =?", (category, )).fetchall()
    sql_connection.close()
    return data


def change_balance(id, Balance):
    sqlite_connection = sqlite3.connect('shop_base.db')
    cursor = sqlite_connection.cursor()

    sql_info_balance = """SELECT balance from users where id = ?"""
    cursor.execute(sql_info_balance, (id,))
    row = cursor.fetchone()
    value = row[0] + Balance
    sql_update_query = """Update users set balance = ? where id = ?"""
    data = (value, id)
    cursor.execute(sql_update_query, data)
    sqlite_connection.commit()

    cursor.close()
    sqlite_connection.close()


def get_info_order():
    sqlite_connection = sqlite3.connect('shop_base.db')
    cursor = sqlite_connection.cursor()

    order_info_arr = []
    sqlite_select_query = """SELECT * from order"""
    cursor.execute(sqlite_select_query)
    rows = cursor.fetchall()
    cursor.close()

    for row in rows:
        order_info = {
        "ID заказа": row[0],
        "ID пользователя": row[1],
        "ФИО": row[2],
        "Номер телефона": row[3],
        "Адрес": row[4],
        "Артикул товара": row[5]
        }
        order_info_arr.append(order_info)
    sqlite_connection.close()

    return order_info_arr


def creating_order(id, FIO, phone, address, art):
    sqlite_connection = sqlite3.connect('shop_base.db')
    cursor = sqlite_connection.cursor()
    # Добавление данных в каталог
    sqlite_insert_with_param = """INSERT INTO orders (id, FIO, number, address, art) VALUES (?, ?, ?, ?, ?);"""
    data_tuple = (id, FIO, phone, address, art)
    cursor.execute(sqlite_insert_with_param, data_tuple)
    sqlite_connection.commit()
    cursor.close()
    sqlite_connection.close()
