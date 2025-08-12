from django.core.management.base import BaseCommand
import json

from planner_api.user import User
from planner_api.team import Team
from planner_api.board import ProjectBoard

class Command(BaseCommand):
    help = "Seed some demo data for quick testing"

    def handle(self, *args, **options):
        u = User()
        t = Team()
        b = ProjectBoard()

        alice = json.loads(u.create_user(json.dumps({"name": "alice", "display_name": "Alice"})))
        bob = json.loads(u.create_user(json.dumps({"name": "bob", "display_name": "Bob"})))
        team = json.loads(t.create_team(json.dumps({
            "name": "alpha",
            "description": "alpha team",
            "admin": alice["id"]
        })))
        t.add_users_to_team(json.dumps({"id": team["id"], "users": [bob["id"]]}))

        board = json.loads(b.create_board(json.dumps({
            "name": "sprint-1",
            "description": "first sprint",
            "team_id": team["id"]
        })))

        task1 = json.loads(b.add_task(json.dumps({
            "title": "setup-ci",
            "description": "set up ci",
            "user_id": alice["id"],
            "board_id": board["id"]
        })))
        task2 = json.loads(b.add_task(json.dumps({
            "title": "readme",
            "description": "write readme",
            "user_id": bob["id"],
            "board_id": board["id"]
        })))

        self.stdout.write(self.style.SUCCESS("Seed done"))
        self.stdout.write(json.dumps({
            "user_ids": [alice["id"], bob["id"]],
            "team_id": team["id"],
            "board_id": board["id"],
            "task_ids": [task1["id"], task2["id"]]
        }, indent=2))
