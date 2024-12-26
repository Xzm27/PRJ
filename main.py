import argparse
import sqlite3
import os
import subprocess
from utils import PrettyTable

# Commands import
from commands.add import AddProject
from commands.list import ListProjects
from commands.open import OpenProject

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
        AddProject(args.name, args.path, args.editor, args.open).run()
    
    elif(args.command == "open"):
        OpenProject(args.name).run()
        
    elif(args.command == "list"):
        ListProjects().run()
        
    else:
        parser.print_help()
        
if __name__ == "__main__":
    main()
    