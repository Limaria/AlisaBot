import psycopg2

import params


def db_connect(user_id):
    con = psycopg2.connect(params.db_params)
    cur = con.cursor()
    cur.execute("SELECT id FROM users WHERE id = %s", (user_id,))

    if not cur.fetchall():
        cur.execute("INSERT INTO users (id, name) VALUES (%s, %s)", (user_id, "Тетя Полли"))
        con.commit()

    print("Record inserted successfully")
    con.close()

def db_orders():
    con = psycopg2.connect(params.db_params)
    cur = con.cursor()
    cur.execute("SELECT user_name, positions, address, id FROM prob WHERE read = %s", (False,))
    ls = cur.fetchall()

    print("просмотренно")
    con.close()
    return ls

def db_orders_read(order_id):
    con = psycopg2.connect(params.db_params)
    cur = con.cursor()
    cur.execute("UPDATE prob set read = %s WHERE id = %s", (True, order_id))
    con.commit()
    print("отправлено")
    con.close()

def db_order_mes_id(mes_id, id):
    con = psycopg2.connect(params.db_params)
    cur = con.cursor()
    cur.execute("UPDATE prob set mes_id = %s WHERE id = %s", (mes_id, id))
    con.commit()
    print('done')
    con.close()

def db_orders_id(user_name):
    con = psycopg2.connect(params.db_params)
    cur = con.cursor()
    cur.execute("SELECT id FROM users WHERE name = %s", (user_name,))
    ls = cur.fetchall()

    print("просмотренно")
    con.close()
    return ls

def db_orders_name(user_name):
    con = psycopg2.connect(params.db_params)
    cur = con.cursor()
    cur.execute("SELECT name FROM users WHERE id = %s", (user_name,))
    ls = cur.fetchall()
    print("просмотренно")
    con.close()
    return ls

def db_done(mes_id):
    con = psycopg2.connect(params.db_params)
    cur = con.cursor()
    cur.execute("UPDATE prob set done = %s WHERE mes_id = %s", (True, mes_id))
    con.commit()
    print('done')
    con.close()


def db_not_done(chat_id):
    con = psycopg2.connect(params.db_params)
    cur = con.cursor()
    cur.execute("SELECT user_name, positions, address, id FROM prob WHERE done = %s AND user_name = %s ", (False, chat_id,))
    ls = cur.fetchall()

    print("не готовые заказы")
    con.close()
    return ls