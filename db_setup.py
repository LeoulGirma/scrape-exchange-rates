# db_setup.py

import sqlite3

def create_database():
    conn = sqlite3.connect('currency_exchange.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS currency_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bank_name TEXT,
        code TEXT,
        name TEXT,
        last_updated TEXT,
        buying REAL,
        selling REAL,
        transaction_buying REAL,
        transaction_selling REAL
    )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
