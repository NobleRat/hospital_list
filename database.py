import sqlite3
from patient import Patient

class Database:
    def __init__(self, db_name="hospital.sqlite3"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS patient (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                age INTEGER,
                diagnosis TEXT,
                cost REAL
            )
        """)
        self.conn.commit()

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM patient")
        rows = self.cursor.fetchall()
        return [Patient(*row) for row in rows]

    def insert(self, patient: Patient):
        self.cursor.execute("""
            INSERT INTO patient (first_name, last_name, age, diagnosis, cost)
            VALUES (?, ?, ?, ?, ?)
        """, patient.as_tuple())
        self.conn.commit()

    def update(self, patient: Patient):
        self.cursor.execute("""
            UPDATE patient SET first_name=?, last_name=?, age=?, diagnosis=?, cost=?
            WHERE id=?
        """, (*patient.as_tuple(), patient.id))
        self.conn.commit()

    def delete(self, patient_id):
        self.cursor.execute("DELETE FROM patient WHERE id=?", (patient_id,))
        self.conn.commit()
