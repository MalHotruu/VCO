import sqlite3


def create_database():
    conn = sqlite3.connect('FilmPortal.db')
    cursor = conn.cursor()

    with open('FilmPortal.sql', 'r') as sql_file:
        sql_script = sql_file.read()

    cursor.executescript(sql_script)
    conn.commit()
    conn.close()


create_database()
