import sqlite3
from configurebot import cfg

db_file = cfg['sqlite_db_path']

def create_connection():
    conn = sqlite3.connect(db_file)
    return conn

def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid INTEGER UNIQUE NOT NULL,
            username TEXT UNIQUE,
            access INTEGER,
            ban INTEGER
        )
    ''')
    conn.commit()
    conn.close()

create_table()

def db_profile_exist(uid):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT 1 FROM profiles WHERE uid = ?', (uid,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def db_profile_exist_usr(username):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT 1 FROM profiles WHERE username = ?', (username,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def db_profile_insertone(uid, username, access, ban):
    conn = create_connection()
    c = conn.cursor()
    c.execute('INSERT INTO profiles (uid, username, access, ban) VALUES (?, ?, ?, ?)', (uid, username, access, ban))
    conn.commit()
    conn.close()

def db_profile_access(uid):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT access FROM profiles WHERE uid = ?', (uid,))
    access = c.fetchone()[0]
    conn.close()
    return access

def db_profile_banned(uid):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT ban FROM profiles WHERE uid = ?', (uid,))
    ban = c.fetchone()[0]
    conn.close()
    return ban == 1

def db_profile_updateone(uid, access=None, ban=None):
    conn = create_connection()
    c = conn.cursor()
    if access is not None:
        c.execute('UPDATE profiles SET access = ? WHERE uid = ?', (access, uid))
    if ban is not None:
        c.execute('UPDATE profiles SET ban = ? WHERE uid = ?', (ban, uid))
    conn.commit()
    conn.close()

def db_profile_get_usrname(username, get):
    conn = create_connection()
    c = conn.cursor()
    c.execute(f'SELECT {get} FROM profiles WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
