import sqlite3

db = sqlite3.connect("blacktalk.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    country TEXT DEFAULT '',
    search_country TEXT DEFAULT 'ANY',
    vip INTEGER DEFAULT 0,
    reports INTEGER DEFAULT 0
)
""")

db.commit()