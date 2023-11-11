import sqlite3 as sq


def start_database():
    global base, cur
    base = sq.connect('database/sqlite_database.db')
    cur = base.cursor()
    if base:
        print('DB connection = Done')
    base.execute("""CREATE TABLE IF NOT EXISTS shop_table(
                photo TEXT,
                name TEXT,
                description TEXT,
                price TEXT)""")
    base.commit()


def add_to_db(data):
    cur.execute("""INSERT INTO shop_table VALUES (?, ?, ?, ?)""", tuple(data.values()))
    base.commit()


def read_db():
    data = cur.execute("""SELECT * FROM shop_table""").fetchall()
    return data

def del_from_db(name):
    cur.execute("""DELETE FROM shop_table WHERE name == ?""", name)
    base.commit()
