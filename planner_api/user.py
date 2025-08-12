import json
from .bases.user_base import UserBase
from .storage import FileStorage

class User(UserBase):
    def __init__(self):
        self.storage = FileStorage()
    
    def create_user(self, request: str) -> str:
        try:
            data = json.loads(request)
            name = data.get('name', '').strip()
            display_name = data.get('display_name', '').strip()
            
            if not name or len(name) > 64:
                raise ValueError("Name is required and must be max 64 characters")
            if len(display_name) > 64:
                raise ValueError("Display name must be max 64 characters")
            
            existing_users = self.storage.filter_by('users', name=name)
            if existing_users:
                raise ValueError("User name must be unique")
            
            user_id = self.storage.create('users', {
                'name': name,
                'display_name': display_name
            })
            
            return json.dumps({"id": user_id})
            
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def list_users(self) -> str:
        users = self.storage.get_all('users')
        result = []
        for user in users:
            result.append({
                'name': user['name'],
                'display_name': user['display_name'],
                'creation_time': user['creation_time']
            })
        return json.dumps(result)
    
    def describe_user(self, request: str) -> str:
        try:
            data = json.loads(request)
            user_id = data.get('id')
            
            if not user_id:
                raise ValueError("User ID is required")
            
            user = self.storage.get('users', user_id)
            if not user:
                raise ValueError("User not found")
            
            return json.dumps({
                'name': user['name'],
                'description': user.get('display_name', ''),
                'creation_time': user['creation_time']
            })
            
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def update_user(self, request: str) -> str:
        try:
            data = json.loads(request)
            user_id = data.get('id')
            user_data = data.get('user', {})
            
            if not user_id:
                raise ValueError("User ID is required")
            
            existing_user = self.storage.get('users', user_id)
            if not existing_user:
                raise ValueError("User not found")
            
            display_name = user_data.get('display_name', '').strip()
            if len(display_name) > 128:
                raise ValueError("Display name must be max 128 characters")
            
            self.storage.update('users', user_id, {
                'display_name': display_name
            })
            
            return json.dumps({"status": "success"})
            
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def get_user_teams(self, request: str) -> str:
        try:
            data = json.loads(request)
            user_id = data.get('id')
            
            if not user_id:
                raise ValueError("User ID is required")
            
            user = self.storage.get('users', user_id)
            if not user:
                raise ValueError("User not found")
            
            user_teams = self.storage.filter_by('user_teams', user_id=user_id)
            result = []
            
            for user_team in user_teams:
                team = self.storage.get('teams', user_team['team_id'])
                if team:
                    result.append({
                        'name': team['name'],
                        'description': team['description'],
                        'creation_time': team['creation_time']
                    })
            
            return json.dumps(result)
            
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
