import sqlite3
import datetime
import secrets

def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            telegram_chat_id TEXT NOT NULL)''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS auth_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            code TEXT NOT NULL,
            expires_at DATETIME NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id))''')

init_db()

def generate_code():
    return ''.join(secrets.choice('0123456789') for _ in range(6))

def check_user_credentials(username, password):
    with sqlite3.connect('database.db') as conn:
        return conn.execute('''SELECT id, telegram_chat_id 
                            FROM users 
                            WHERE username = ? AND password_hash = ?''',
                            (username, password)).fetchone()

def save_user(username, password, chat_id):
    with sqlite3.connect('database.db') as conn:
        conn.execute('INSERT INTO users(username, password_hash, telegram_chat_id) VALUES (?, ?, ?)',
                    (username, password, chat_id))

def save_auth_code(user_id, code, expires_at):
    with sqlite3.connect('database.db') as conn:
        conn.execute('INSERT INTO auth_codes(user_id, code, expires_at) VALUES (?, ?, ?)',
                    (user_id, code, expires_at.isoformat()))

def verify_code(code):
    with sqlite3.connect('database.db') as conn:
        record = conn.execute('''SELECT user_id 
                               FROM auth_codes 
                               WHERE code = ? AND expires_at > datetime('now')''',
                             (code,)).fetchone()
        if record:
            conn.execute('DELETE FROM auth_codes WHERE code = ?', (code,))
        return bool(record)

