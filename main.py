import argparse
import sqlite3
import os
import subprocess
from prettytable import PrettyTable

db = "projects.db"

def init_db()-> None:
    """
    Initializes the database
    """
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
    
def validate_path(path: str) -> str:
    """
    Validates or creates the given path.

    Args:
        path (str): The path to validate or create.

    Returns:
        str: Absolute, resolved path if valid or created.
    """
    abs_path = os.path.abspath(path)
    resolved_path = os.path.realpath(abs_path)
    
    if not os.path.exists(resolved_path):
        print(f"Path '{resolved_path}' does not exist. Creating it...")
        os.makedirs(resolved_path)
    elif not os.path.isdir(resolved_path):
        print(f"Error: Path '{resolved_path}' is not a directory.")
        return None

    if not os.access(resolved_path, os.W_OK):
        print(f"Error: Path '{resolved_path}' is not writable.")
        return None

    return resolved_path
    
def add_project(name: str, path: str, editor: str="nano", open_flag: bool=False)-> None:
    """
    Adds a project to the database
    
    Args:
        name (str): Name of the project
        path (str): Project path
        editor (str): Preferred editor for the project (defualt: nano)
        open_flag (bool): Flag to check if the project will be opened on adition
    """
    
    resolved_path = validate_path(path)
    
    if not resolved_path:
        return
    
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    # Check if the project already exists
    cursor.execute("SELECT * FROM projects WHERE name = ? OR path = ?", (name, resolved_path))
    if cursor.fetchone():
        print(f"Error: A project with the name '{name}' or path '{resolved_path}' already exists.")
        conn.close()
        return

    # Insert the new project with timestamp and editor
    cursor.execute(
        "INSERT INTO projects (name, path, editor) VALUES (?, ?, ?)",
        (name, resolved_path, editor)
    )
    conn.commit()
    conn.close()
    print(f"Added project '{name}' at '{resolved_path}' with editor '{editor}'")
    
    if open_flag:
        open_project(name)
    
def open_project(name: str)-> None:
    """
    Opens a project
    
    Args:
        name (str): name of the project to be opened
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
        
def list_projects()-> None:
    """
    Lists all the project
    """
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
    """
    Main function
    """
    init_db()
    
    parser = argparse.ArgumentParser(prog="PRJ", description="CLI Tool to manage coding projects")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Add projects command
    add_parser = subparsers.add_parser("add", help="Add project")
    add_parser.add_argument("name", help="Project name")
    add_parser.add_argument("path", nargs="?", default=".", help="Project path (default: current directory)")    
    add_parser.add_argument("--editor", default="nano", help="Preferred editor (default: nano)")
    add_parser.add_argument("-o", "--open", action="store_true", help="Open project after adding")
    
    # Open projects command
    open_parser = subparsers.add_parser("open", help="Open project")
    open_parser.add_argument("name", help="Project name")
    
    # List projects command
    list_parser = subparsers.add_parser("list", help="List projects")
    
    args = parser.parse_args()
    
    if(args.command == "add"):
        add_project(args.name, args.path, args.editor, args.open)
    
    elif(args.command == "open"):
        open_project(args.name)
        
    elif(args.command == "list"):
        list_projects()
        
    else:
        parser.print_help()
        
if __name__ == "__main__":
    main()
    