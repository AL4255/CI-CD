

# Vulnerbale-web app 
from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)


def init_db()

    conn = sqlite3.connet('users.db')

    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMAY KEY,
        username TEXT,
        password TEXT
        email TEXT
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'password123', 'admin@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users VAULES (2, 'Uuser', 'userpass', 'user@example.com)")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (3, 'guest', 'guest123', guest@example.com)")
    conn.commit()
    conn.close()
