from django.urls import path
from .views import (
    QuizListCreateView, QuizDetailView,
    QuestionListCreateView, QuestionDetailView,
    QuizSubmitView, LeaderboardView
)

urlpatterns = [
    path('quizzes/', QuizListCreateView.as_view(), name='quiz-list-create'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('submit-quiz/<int:quiz_id>/', QuizSubmitView.as_view(), name='submit-quiz'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]
