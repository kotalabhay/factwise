import json
import os
from datetime import datetime
from .bases.project_board_base import ProjectBoardBase
from .storage import FileStorage

class ProjectBoard(ProjectBoardBase):
    def __init__(self):
        self.storage = FileStorage()
    
    def create_board(self, request: str):
        try:
            data = json.loads(request)
            name = data.get('name', '').strip()
            description = data.get('description', '').strip()
            team_id = data.get('team_id')
            
            if not name or len(name) > 64:
                raise ValueError("Name is required and must be max 64 characters")
            if len(description) > 128:
                raise ValueError("Description must be max 128 characters")
            if not team_id:
                raise ValueError("Team ID is required")
            
            team = self.storage.get('teams', team_id)
            if not team:
                raise ValueError("Team not found")
            
            existing_boards = self.storage.filter_by('boards', team_id=team_id, name=name)
            if existing_boards:
                raise ValueError("Board name must be unique for a team")
            
            board_id = self.storage.create('boards', {
                'name': name,
                'description': description,
                'team_id': team_id,
                'status': 'OPEN'
            })
            
            return json.dumps({"id": board_id})
            
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def close_board(self, request: str) -> str:
        try:
            data = json.loads(request)
            board_id = data.get('id')
            
            if not board_id:
                raise ValueError("Board ID is required")
            
            board = self.storage.get('boards', board_id)
            if not board:
                raise ValueError("Board not found")
            
            tasks = self.storage.filter_by('tasks', board_id=board_id)
            for task in tasks:
                if task.get('status') != 'COMPLETE':
                    raise ValueError("Cannot close board with incomplete tasks")
            
            self.storage.update('boards', board_id, {
                'status': 'CLOSED',
                'end_time': datetime.now().isoformat()
            })
            
            return json.dumps({"status": "success"})
            
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def add_task(self, request: str) -> str:
        try:
            data = json.loads(request)
            title = data.get('title', '').strip()
            description = data.get('description', '').strip()
            user_id = data.get('user_id')
            board_id = data.get('board_id')
            
            if not title or len(title) > 64:
                raise ValueError("Title is required and must be max 64 characters")
            if len(description) > 128:
                raise ValueError("Description must be max 128 characters")
            if not user_id:
                raise ValueError("User ID is required")
            if not board_id:
                raise ValueError("Board ID is required")
            
            board = self.storage.get('boards', board_id)
            if not board:
                raise ValueError("Board not found")
            if board.get('status') != 'OPEN':
                raise ValueError("Can only add tasks to open boards")
            
            user = self.storage.get('users', user_id)
            if not user:
                raise ValueError("User not found")
            
            existing_tasks = self.storage.filter_by('tasks', board_id=board_id, title=title)
            if existing_tasks:
                raise ValueError("Task title must be unique for a board")
            
            task_id = self.storage.create('tasks', {
                'title': title,
                'description': description,
                'user_id': user_id,
                'board_id': board_id,
                'status': 'OPEN'
            })
            
            return json.dumps({"id": task_id})
            
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def update_task_status(self, request: str):
        try:
            data = json.loads(request)
            task_id = data.get('id')
            status = data.get('status')
            
            if not task_id:
                raise ValueError("Task ID is required")
            if status not in ['OPEN', 'IN_PROGRESS', 'COMPLETE']:
                raise ValueError("Status must be OPEN, IN_PROGRESS, or COMPLETE")
            
            task = self.storage.get('tasks', task_id)
            if not task:
                raise ValueError("Task not found")
            
            self.storage.update('tasks', task_id, {'status': status})
            return json.dumps({"status": "success"})
            
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def list_boards(self, request: str) -> str:
        try:
            data = json.loads(request)
            team_id = data.get('id')
            
            if not team_id:
                raise ValueError("Team ID is required")
            
            team = self.storage.get('teams', team_id)
            if not team:
                raise ValueError("Team not found")
            
            boards = self.storage.filter_by('boards', team_id=team_id, status='OPEN')
            result = []
            
            for board in boards:
                result.append({
                    'id': board['id'],
                    'name': board['name']
                })
            
            return json.dumps(result)
            
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def export_board(self, request: str) -> str:
        try:
            data = json.loads(request)
            board_id = data.get('id')
            
            if not board_id:
                raise ValueError("Board ID is required")
            
            board = self.storage.get('boards', board_id)
            if not board:
                raise ValueError("Board not found")
            
            tasks = self.storage.filter_by('tasks', board_id=board_id)
            
            os.makedirs('out', exist_ok=True)
            filename = f"board_{board_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filepath = os.path.join('out', filename)
            
            with open(filepath, 'w') as f:
                f.write(f"BOARD EXPORT REPORT\n")
                f.write(f"==================\n\n")
                f.write(f"Board: {board['name']}\n")
                f.write(f"Description: {board['description']}\n")
                f.write(f"Status: {board['status']}\n")
                f.write(f"Created: {board['creation_time']}\n")
                if board.get('end_time'):
                    f.write(f"Closed: {board['end_time']}\n")
                f.write(f"\nTASKS ({len(tasks)} total)\n")
                f.write(f"{'='*50}\n\n")
                
                status_counts = {'OPEN': 0, 'IN_PROGRESS': 0, 'COMPLETE': 0}
                
                for i, task in enumerate(tasks, 1):
                    user = self.storage.get('users', task['user_id'])
                    user_name = user['name'] if user else 'Unknown User'
                    status = task.get('status', 'OPEN')
                    status_counts[status] += 1
                    
                    f.write(f"{i}. {task['title']} [{status}]\n")
                    f.write(f"   Assigned to: {user_name}\n")
                    f.write(f"   Description: {task['description']}\n")
                    f.write(f"   Created: {task['creation_time']}\n")
                    f.write(f"\n")
                
                f.write(f"\nSUMMARY\n")
                f.write(f"-------\n")
                f.write(f"Open: {status_counts['OPEN']}\n")
                f.write(f"In Progress: {status_counts['IN_PROGRESS']}\n")
                f.write(f"Complete: {status_counts['COMPLETE']}\n")
                f.write(f"Total: {sum(status_counts.values())}\n")
            
            return json.dumps({"out_file": filename})
            
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
