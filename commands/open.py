from .base import PRJ
import subprocess
import os

class OpenProject(PRJ):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        
    def run(self):
        """Run a project"""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT path, editor FROM PROJECTS WHERE name = ?", (self.name,))
            result = cursor.fetchone()
            
        if result:
            project_path, editor = result
            if os.path.exists(project_path):
                # Open the project path with nano
                print(f"Opening project: {self.name} path: {project_path}")
                subprocess.run([editor, project_path])
            else:
                print(f"Error: Path '{project_path}' does not exist.")
        else:
            print(f"Error: No project found with the name '{self.name}'")