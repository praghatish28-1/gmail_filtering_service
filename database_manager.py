import sqlite3
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id TEXT PRIMARY KEY,
                sender TEXT,
                subject TEXT,
                body TEXT,
                received_at TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def store_email(self, email_id, sender, subject, body, received_at):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO emails (id, sender, subject, body, received_at) 
            VALUES (?, ?, ?, ?, ?)
        ''', (email_id, sender, subject, body, received_at))
        conn.commit()
        conn.close()

    def get_emails(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM emails')
        emails = cursor.fetchall()
        conn.close()
        return [{
            'id': email[0],
            'From': email[1],
            'Subject': email[2],
            'Body': email[3],
            'Date received': email[4]
        } for email in emails]
