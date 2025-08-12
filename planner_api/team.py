import json
from .bases.team_base import TeamBase
from .storage import FileStorage

class Team(TeamBase):
    def __init__(self):
        self.storage = FileStorage()
    
    def create_team(self, request: str) -> str:
        try:
            data = json.loads(request)
            name = data.get('name', '').strip()
            description = data.get('description', '').strip()
            admin = data.get('admin')
            
            if not name or len(name) > 64:
                raise ValueError("Name is required and must be max 64 characters")
            if len(description) > 128:
                raise ValueError("Description must be max 128 characters")
            if not admin:
                raise ValueError("Admin user ID is required")
            
            admin_user = self.storage.get('users', admin)
            if not admin_user:
                raise ValueError("Admin user not found")
            
            existing_teams = self.storage.filter_by('teams', name=name)
            if existing_teams:
                raise ValueError("Team name must be unique")
            
            team_id = self.storage.create('teams', {
                'name': name,
                'description': description,
                'admin': admin
            })
            
            self.storage.create('user_teams', {
                'user_id': admin,
                'team_id': team_id
            })
            
            return json.dumps({"id": team_id})
            
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def list_teams(self) -> str:
        teams = self.storage.get_all('teams')
        result = []
        for team in teams:
            result.append({
                'name': team['name'],
                'description': team['description'],
                'creation_time': team['creation_time'],
                'admin': team['admin']
            })
        return json.dumps(result)
    
    def describe_team(self, request: str) -> str:
        try:
            data = json.loads(request)
            team_id = data.get('id')
            
            if not team_id:
                raise ValueError("Team ID is required")
            
            team = self.storage.get('teams', team_id)
            if not team:
                raise ValueError("Team not found")
            
            return json.dumps({
                'name': team['name'],
                'description': team['description'],
                'creation_time': team['creation_time'],
                'admin': team['admin']
            })
            
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def update_team(self, request: str) -> str:
        try:
            data = json.loads(request)
            team_id = data.get('id')
            team_data = data.get('team', {})
            
            if not team_id:
                raise ValueError("Team ID is required")
            
            existing_team = self.storage.get('teams', team_id)
            if not existing_team:
                raise ValueError("Team not found")
            
            name = team_data.get('name', '').strip()
            description = team_data.get('description', '').strip()
            admin = team_data.get('admin')
            
            if name and len(name) > 64:
                raise ValueError("Name must be max 64 characters")
            if len(description) > 128:
                raise ValueError("Description must be max 128 characters")
            
            if name and name != existing_team['name']:
                existing_teams = self.storage.filter_by('teams', name=name)
                if existing_teams:
                    raise ValueError("Team name must be unique")
            
            if admin:
                admin_user = self.storage.get('users', admin)
                if not admin_user:
                    raise ValueError("Admin user not found")
            
            update_data = {}
            if name:
                update_data['name'] = name
            if description:
                update_data['description'] = description
            if admin:
                update_data['admin'] = admin
            
            self.storage.update('teams', team_id, update_data)
            return json.dumps({"status": "success"})
            
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def add_users_to_team(self, request: str):
        try:
            data = json.loads(request)
            team_id = data.get('id')
            users = data.get('users', [])
            
            if not team_id:
                raise ValueError("Team ID is required")
            if not users:
                raise ValueError("Users list is required")
            
            team = self.storage.get('teams', team_id)
            if not team:
                raise ValueError("Team not found")
            
            current_members = self.storage.filter_by('user_teams', team_id=team_id)
            if len(current_members) + len(users) > 50:
                raise ValueError("Cannot exceed 50 users per team")
            
            for user_id in users:
                user = self.storage.get('users', user_id)
                if not user:
                    raise ValueError(f"User {user_id} not found")
                
                existing_membership = self.storage.filter_by('user_teams', user_id=user_id, team_id=team_id)
                if not existing_membership:
                    self.storage.create('user_teams', {
                        'user_id': user_id,
                        'team_id': team_id
                    })
            
            return json.dumps({"status": "success"})
            
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def remove_users_from_team(self, request: str):
        try:
            data = json.loads(request)
            team_id = data.get('id')
            users = data.get('users', [])
            
            if not team_id:
                raise ValueError("Team ID is required")
            if not users:
                raise ValueError("Users list is required")
            
            team = self.storage.get('teams', team_id)
            if not team:
                raise ValueError("Team not found")
            
            for user_id in users:
                if user_id == team['admin']:
                    raise ValueError("Cannot remove team admin")
                
                memberships = self.storage.filter_by('user_teams', user_id=user_id, team_id=team_id)
                for membership in memberships:
                    self.storage.delete('user_teams', membership['id'])
            
            return json.dumps({"status": "success"})
            
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def list_team_users(self, request: str):
        try:
            data = json.loads(request)
            team_id = data.get('id')
            
            if not team_id:
                raise ValueError("Team ID is required")
            
            team = self.storage.get('teams', team_id)
            if not team:
                raise ValueError("Team not found")
            
            user_teams = self.storage.filter_by('user_teams', team_id=team_id)
            result = []
            
            for user_team in user_teams:
                user = self.storage.get('users', user_team['user_id'])
                if user:
                    result.append({
                        'id': user['id'],
                        'name': user['name'],
                        'display_name': user['display_name']
                    })
            
            return json.dumps(result)
            
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
