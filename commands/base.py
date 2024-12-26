import sqlite3

DB_NAME = "projects.db"


class PRJ:
    def __init__(self, db_name: str = DB_NAME):
        self.db_name: str = db_name
        
    def connect(self):
        """Establish and return database connection"""
        conn = sqlite3.connect(self.db_name)
        return conn
    
    def project_exists(self, name: str, path: str) -> bool:
        """Check if a project with a given name or path already exists"""
        query: str = "SELECT 1 from PROJECTS where name = ? or path = ?"
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (name, path))
            
            return cursor.fetchone() is not None
        
    def insert_project(self, name: str, path: str, editor: str)-> None:
        """Inserts a project into the database"""
        query: str = "INSERT into PROJECTS (name, path, editor) VALUES (?, ?, ?)"
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (name, path, editor))
            conn.commit()
             
        
            