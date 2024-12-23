import argparse
import sqlite3
import os
import subprocess
from prettytable import PrettyTable

db = "projects.db"

def init_db():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        path TEXT NOT NULL UNIQUE,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        editor TEXT DEFAULT 'nano'
    )
    """)
    conn.commit()
    conn.close()
    
def add_project(name, path, editor="nano"):
    # Check if the path exists and is a directory
    if not os.path.exists(path):
        print(f"Error: Path '{path}' does not exist.")
        return
    if not os.path.isdir(path):
        print(f"Error: Path '{path}' is not a directory.")
        return

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    # Check if the project already exists
    cursor.execute("SELECT * FROM projects WHERE name = ? OR path = ?", (name, path))
    if cursor.fetchone():
        print(f"Error: A project with the name '{name}' or path '{path}' already exists.")
        conn.close()
        return

    # Insert the new project with timestamp and editor
    cursor.execute(
        "INSERT INTO projects (name, path, editor) VALUES (?, ?, ?)",
        (name, path, editor)
    )
    conn.commit()
    conn.close()
    print(f"Added project '{name}' at '{path}' with editor '{editor}'")
    
def open_project(name):
    """
    Opens a project
    """
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    # Fetch the project by name
    cursor.execute("SELECT path, editor FROM projects WHERE name = ?", (name,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        project_path, editor = result
        if os.path.exists(project_path):
            # Open the project path with nano
            print(f"Opening project: {name} path: {project_path}")
            subprocess.run([editor, project_path])
        else:
            print(f"Error: Path '{project_path}' does not exist.")
    else:
        print(f"Error: No project found with the name '{name}'")
        
def list_projects():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    # Fetch all the projects
    cursor.execute("SELECT name, path from projects")
    result = cursor.fetchall()
    conn.close()
    
    if(result):
        headers = ["Name", "Path"]
        table = PrettyTable(headers, result)
        
        print(table.get_table())
        
    else:
        print("no projects to show")

def main():
    init_db()
    
    parser = argparse.ArgumentParser(prog="PRJ", description="CLI Tool to manage coding projects")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Add projects command
    add_parser = subparsers.add_parser("add", help="Add project")
    add_parser.add_argument("name", help="Project name")
    add_parser.add_argument("path", help="Project path")
    add_parser.add_argument("--editor", default="nano", help="Preferred editor (default: nano)")
    
    # Open projects command
    open_parser = subparsers.add_parser("open", help="Open project")
    open_parser.add_argument("name", help="Project name")
    
    # List projects command
    list_parser = subparsers.add_parser("list", help="List projects")
    
    args = parser.parse_args()
    
    if(args.command == "add"):
        add_project(args.name, args.path, args.editor)
    
    elif(args.command == "open"):
        open_project(args.name)
        
    elif(args.command == "list"):
        list_projects()
        
    else:
        parser.print_help()
        
if __name__ == "__main__":
    main()
    