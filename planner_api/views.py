from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import json

from .user import User
from .team import Team
from .board import ProjectBoard

class UserCreateView(APIView):
    def post(self, request):
        try:
            user_impl = User()
            result = user_impl.create_user(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    def get(self, request):
        try:
            user_impl = User()
            result = user_impl.list_users()
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    def post(self, request):
        try:
            user_impl = User()
            result = user_impl.describe_user(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateView(APIView):
    def put(self, request):
        try:
            user_impl = User()
            result = user_impl.update_user(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserTeamsView(APIView):
    def post(self, request):
        try:
            user_impl = User()
            result = user_impl.get_user_teams(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TeamCreateView(APIView):
    def post(self, request):
        try:
            team_impl = Team()
            result = team_impl.create_team(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TeamListView(APIView):
    def get(self, request):
        try:
            team_impl = Team()
            result = team_impl.list_teams()
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TeamDetailView(APIView):
    def post(self, request):
        try:
            team_impl = Team()
            result = team_impl.describe_team(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TeamUpdateView(APIView):
    def put(self, request):
        try:
            team_impl = Team()
            result = team_impl.update_team(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TeamAddUsersView(APIView):
    def post(self, request):
        try:
            team_impl = Team()
            result = team_impl.add_users_to_team(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TeamRemoveUsersView(APIView):
    def post(self, request):
        try:
            team_impl = Team()
            result = team_impl.remove_users_from_team(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TeamUsersView(APIView):
    def post(self, request):
        try:
            team_impl = Team()
            result = team_impl.list_team_users(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BoardCreateView(APIView):
    def post(self, request):
        try:
            board_impl = ProjectBoard()
            result = board_impl.create_board(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BoardCloseView(APIView):
    def post(self, request):
        try:
            board_impl = ProjectBoard()
            result = board_impl.close_board(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TaskCreateView(APIView):
    def post(self, request):
        try:
            board_impl = ProjectBoard()
            result = board_impl.add_task(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TaskUpdateView(APIView):
    def put(self, request):
        try:
            board_impl = ProjectBoard()
            result = board_impl.update_task_status(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BoardListView(APIView):
    def post(self, request):
        try:
            board_impl = ProjectBoard()
            result = board_impl.list_boards(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BoardExportView(APIView):
    def post(self, request):
        try:
            board_impl = ProjectBoard()
            result = board_impl.export_board(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
