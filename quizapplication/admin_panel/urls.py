from django.urls import path
from .views import (
    AdminLoginView, AdminUserListView, AdminUserDetailView,
    AdminQuizListView, AdminQuizDetailView,
    AdminQuestionListView, AdminQuestionDetailView
)

urlpatterns = [
    path("login/", AdminLoginView.as_view(), name="admin-login"),
    path("users/", AdminUserListView.as_view(), name="admin-user-list"),
    path("users/<int:pk>/", AdminUserDetailView.as_view(), name="admin-user-detail"),
    path("quizzes/", AdminQuizListView.as_view(), name="admin-quiz-list"),
    path("quizzes/<int:pk>/", AdminQuizDetailView.as_view(), name="admin-quiz-detail"),
    path("questions/", AdminQuestionListView.as_view(), name="admin-question-list"),
    path("questions/<int:pk>/", AdminQuestionDetailView.as_view(), name="admin-question-detail"),
]
