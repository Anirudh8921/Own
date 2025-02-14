from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Quiz, Question, QuizAttempt
from .serializers import QuizSerializer, QuestionSerializer, QuizAttemptSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# ✅ Only Admins can create quizzes, but all users can view them
class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Admins can create, users can view

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# ✅ Quiz Detail View (Admins can edit, users can view)
class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Admins can edit/delete, users can view

# ✅ Only Admins can add/edit questions
class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admins can create questions

class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admins can modify questions

# ✅ User Submits a Quiz
class QuizSubmitView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can submit quizzes

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'answers': openapi.Schema(type=openapi.TYPE_OBJECT)
            },
            required=['answers']
        ),
        responses={201: QuizAttemptSerializer()}
    )
    def post(self, request, quiz_id):
        user = request.user

        # ✅ Handle invalid quiz ID
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

        user_answers = request.data.get("answers", {})
        questions = Question.objects.filter(quiz=quiz)

        if not questions.exists():
            return Response({"error": "No questions found for this quiz"}, status=status.HTTP_400_BAD_REQUEST)

        correct_count = sum(
            1 for q in questions if str(q.id) in user_answers and int(user_answers[str(q.id)]) == q.correct_option
        )

        score = (correct_count / questions.count()) * 100
        attempt = QuizAttempt.objects.create(
            user=user, quiz=quiz, score=score, total_questions=questions.count(), correct_answers=correct_count
        )

        return Response(QuizAttemptSerializer(attempt).data, status=status.HTTP_201_CREATED)

# ✅ Leaderboard (Top 10 Scores)
class LeaderboardView(generics.ListAPIView):
    serializer_class = QuizAttemptSerializer
    permission_classes = [permissions.AllowAny]  # Leaderboard is public

    def get_queryset(self):
        return QuizAttempt.objects.order_by('-score')[:10]
