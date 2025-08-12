from django.urls import path
from .views import (
    UserCreateView, UserListView, UserDetailView, UserUpdateView, UserTeamsView,
    TeamCreateView, TeamListView, TeamDetailView, TeamUpdateView, TeamAddUsersView, TeamRemoveUsersView, TeamUsersView,
    BoardCreateView, BoardCloseView, TaskCreateView, TaskUpdateView, BoardListView, BoardExportView,
)

urlpatterns = [
    # Users
    path('users/create', UserCreateView.as_view()),
    path('users', UserListView.as_view()),
    path('users/describe', UserDetailView.as_view()),
    path('users/update', UserUpdateView.as_view()),
    path('users/teams', UserTeamsView.as_view()),

    # Teams
    path('teams/create', TeamCreateView.as_view()),
    path('teams', TeamListView.as_view()),
    path('teams/describe', TeamDetailView.as_view()),
    path('teams/update', TeamUpdateView.as_view()),
    path('teams/add-users', TeamAddUsersView.as_view()),
    path('teams/remove-users', TeamRemoveUsersView.as_view()),
    path('teams/users', TeamUsersView.as_view()),

    # Boards / Tasks
    path('boards/create', BoardCreateView.as_view()),
    path('boards/close', BoardCloseView.as_view()),
    path('boards/list', BoardListView.as_view()),
    path('boards/export', BoardExportView.as_view()),

    path('tasks/create', TaskCreateView.as_view()),
    path('tasks/update', TaskUpdateView.as_view()),
]
