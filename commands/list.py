from .base import PRJ
from utils import PrettyTable

class ListProjects(PRJ):
    def __init__(self):
        super().__init__()
        
    def run(self):
        """Show all the projects"""
        # TODO: Check if all the paths exists (if any paths have been deleted)
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, path, timestamp, editor from PROJECTS")
            result = cursor.fetchall()
            
        if result:
            headers = ["Name", "Path", "Timestamp", "Editor"]
            table = PrettyTable(headers, result)
            
            print(table.get_table())
            
        else:
            print("No projects to show")
                
            