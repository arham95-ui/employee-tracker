import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="employee_logs.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()
    
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employee_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_name TEXT,
                event_type TEXT,
                photo_path TEXT,
                timestamp TEXT,
                status TEXT
            )
        ''')
        self.conn.commit()
    
    def log_event(self, employee_name, event_type, photo_path="", status=""):
        cursor = self.conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO employee_activity 
            (employee_name, event_type, photo_path, timestamp, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (employee_name, event_type, photo_path, timestamp, status))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_recent_logs(self, limit=10):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM employee_activity 
            ORDER BY timestamp DESC LIMIT ?
        ''', (limit,))
        return cursor.fetchall()
    
    def close(self):
        self.conn.close()