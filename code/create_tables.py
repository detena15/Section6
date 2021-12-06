import sqlite3

con = sqlite3.connect('data.db')
cursor = con.cursor()

users_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"  # al usar INTEGER, se crea id de forma incremental
cursor.execute(users_table)

items_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(items_table)

con.commit()

con.close()
