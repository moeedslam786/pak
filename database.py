import sqlite3
import logging
from datetime import datetime

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                # Users table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        balance REAL DEFAULT 0.0,
                        language TEXT DEFAULT 'en',
                        referrer_id INTEGER,
                        joined_date TIMESTAMP,
                        last_mining TIMESTAMP
                    )
                ''')

                # Mining history
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS mining_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        amount REAL,
                        timestamp TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    )
                ''')

                # Tasks table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        task_type TEXT,
                        completed BOOLEAN DEFAULT FALSE,
                        completion_date TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    )
                ''')

                conn.commit()
        except Exception as e:
            logging.error(f"Database initialization error: {e}")

    def add_user(self, user_id, username, referrer_id=None):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT OR IGNORE INTO users (user_id, username, referrer_id, joined_date) VALUES (?, ?, ?, ?)',
                    (user_id, username, referrer_id, datetime.now())
                )
                conn.commit()
                return True
        except Exception as e:
            logging.error(f"Error adding user: {e}")
            return False

    def update_balance(self, user_id, amount):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'UPDATE users SET balance = balance + ? WHERE user_id = ?',
                    (amount, user_id)
                )
                conn.commit()
                return True
        except Exception as e:
            logging.error(f"Error updating balance: {e}")
            return False

    def get_user(self, user_id):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
                return cursor.fetchone()
        except Exception as e:
            logging.error(f"Error getting user: {e}")
            return None

    def update_last_mining(self, user_id):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'UPDATE users SET last_mining = ? WHERE user_id = ?',
                    (datetime.now(), user_id)
                )
                conn.commit()
                return True
        except Exception as e:
            logging.error(f"Error updating last mining: {e}")
            return False
