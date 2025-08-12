import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Any

class FileStorage:
    def __init__(self, db_dir: str = "db"):
        self.db_dir = db_dir
        os.makedirs(db_dir, exist_ok=True)
        
    def _get_file_path(self, entity_type: str) -> str:
        return os.path.join(self.db_dir, f"{entity_type}.json")
    
    def _load_data(self, entity_type: str) -> Dict[str, Any]:
        file_path = self._get_file_path(entity_type)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_data(self, entity_type: str, data: Dict[str, Any]):
        file_path = self._get_file_path(entity_type)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def create(self, entity_type: str, data: Dict[str, Any]) -> str:
        entity_id = str(uuid.uuid4())
        all_data = self._load_data(entity_type)
        data['id'] = entity_id
        data['creation_time'] = datetime.now().isoformat()
        all_data[entity_id] = data
        self._save_data(entity_type, all_data)
        return entity_id
    
    def get(self, entity_type: str, entity_id: str) -> Dict[str, Any]:
        all_data = self._load_data(entity_type)
        return all_data.get(entity_id)
    
    def get_all(self, entity_type: str) -> List[Dict[str, Any]]:
        all_data = self._load_data(entity_type)
        return list(all_data.values())
    
    def update(self, entity_type: str, entity_id: str, data: Dict[str, Any]):
        all_data = self._load_data(entity_type)
        if entity_id in all_data:
            all_data[entity_id].update(data)
            self._save_data(entity_type, all_data)
            return True
        return False
    
    def delete(self, entity_type: str, entity_id: str):
        all_data = self._load_data(entity_type)
        if entity_id in all_data:
            del all_data[entity_id]
            self._save_data(entity_type, all_data)
            return True
        return False
    
    def filter_by(self, entity_type: str, **filters) -> List[Dict[str, Any]]:
        all_data = self._load_data(entity_type)
        results = []
        for item in all_data.values():
            match = True
            for key, value in filters.items():
                if key not in item or item[key] != value:
                    match = False
                    break
            if match:
                results.append(item)
        return results
