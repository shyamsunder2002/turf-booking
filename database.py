import sqlite3

def get_db():
    conn = sqlite3.connect('turf.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'customer'
        );

        CREATE TABLE IF NOT EXISTS turfs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            price_per_hour REAL NOT NULL,
            available INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            turf_id INTEGER,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(turf_id) REFERENCES turfs(id)
        );
    ''')

    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
               ('admin', '$2b$12$ZwBJ2eG5S/VsSR0SfQxE1.K/NyeVYLscKFH.l8RqGi9A.UK9W8LbS', 'admin'))

    cursor.execute("SELECT COUNT(*) FROM turfs")
    if cursor.fetchone()[0] == 0:
        turfs = [
            ('Greenfield Turf', 'Dublin North', 25.0),
            ('City Arena', 'Dublin South', 30.0),
            ('Phoenix Park Pitch', 'Dublin West', 20.0),
        ]
        cursor.executemany("INSERT INTO turfs (name, location, price_per_hour) VALUES (?,?,?)", turfs)

    conn.commit()
    conn.close()