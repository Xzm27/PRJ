from .base import PRJ
from utils import validate_path

class AddProject(PRJ):
    def __init__(self, name: str, path: str, editor: str = "nano", open_flag: bool = False):
        super().__init__()
        self.name: str = name
        self.path: str = path
        self.editor: str = editor
        self.open_flag: str = open_flag
        
    def run(self):
        """Run the add command"""
        resolved_path = validate_path(self.path)
        
        if not resolved_path:
            return
        
        if self.project_exists(self.name, resolved_path):
            print(f"Error: A project with name {self.name} or path {resolved_path} already exists")
            return
        
        self.insert_project(self.name, resolved_path, self.editor)
        print(f"Added project '{self.name}' at '{resolved_path}' with editor '{self.editor}'")