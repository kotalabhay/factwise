# Team Project Planner API (DRF)

Implements the ProblemStatement using Django REST Framework. JSON-only endpoints for users, teams, project boards, and tasks. Data persists to local files under `db/`.

## Structure

- `planner_api/storage.py` simple JSON file store
- `planner_api/user.py`, `planner_api/team.py`, `planner_api/board.py` implement base API behavior
- `planner_api/bases/` contains abstract base interfaces used by implementations
- `planner_api/views.py`, `planner_api/urls.py` DRF glue
- `project_planner/` Django project config
- `db/` created on first write, `out/` holds board exports

## Install & run (Windows PowerShell)

```
# 1) Create and activate venv
python -m venv .venv
.venv\\Scripts\\Activate.ps1

# 2) Install deps
pip install -r requirements.txt

# 3) Seed demo data (optional)
python manage.py seed_demo

# 4) Start server
python manage.py runserver
```

Base path: `http://127.0.0.1:8000/api/`

## Endpoints (JSON)

Users
- POST `/api/users/create` {"name","display_name"} -> {"id"}
- GET `/api/users`
- POST `/api/users/describe` {"id"}
- PUT `/api/users/update` {"id","user":{"display_name"}}
- POST `/api/users/teams` {"id"}

Teams
- POST `/api/teams/create` {"name","description","admin"} -> {"id"}
- GET `/api/teams`
- POST `/api/teams/describe` {"id"}
- PUT `/api/teams/update` {"id","team":{"name?","description?","admin?"}}
- POST `/api/teams/add-users` {"id","users":["<user_id>",...]}
- POST `/api/teams/remove-users` {"id","users":[...]}
- POST `/api/teams/users` {"id"}

Boards/Tasks
- POST `/api/boards/create` {"name","description","team_id"} -> {"id"}
- POST `/api/boards/close` {"id"}
- POST `/api/boards/list` {"id":"<team_id>"}
- POST `/api/boards/export` {"id"} -> {"out_file"}
- POST `/api/tasks/create` {"title","description","user_id","board_id"} -> {"id"}
- PUT `/api/tasks/update` {"id","status":"OPEN|IN_PROGRESS|COMPLETE"}

## Demo data

Run `python manage.py seed_demo` to create two users, one team, one board, and two tasks.

## Constraints enforced

- Uniqueness: user.name, team.name, board.name per team, task.title per board
- Length caps per docstrings
- Team user cap 50; cannot remove admin
- Add task only to OPEN boards; close board only if all tasks COMPLETE; set end_time

## Challenges

- Uniqueness/caps without DB: handled via `filter_by()` over JSON files
- Board lifecycle: explicit checks before write
- Keep it small and readable: thin views, clear validations, simple storage
