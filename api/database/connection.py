# database/connection.py
import sqlite3

def get_db():
    conn = sqlite3.connect('filmes.db')
    conn.row_factory = sqlite3.Row
    return conn


    