from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import AdminUser
from quiz.models import User, Quiz, Question
from .serializers import (
    AdminLoginSerializer, AdminUserSerializer,
    UserSerializer, QuizSerializer, QuestionSerializer
)

# Admin Login View
class AdminLoginView(APIView):
    @swagger_auto_schema(
        request_body=AdminLoginSerializer,
        responses={200: openapi.Response(
            "Success", openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING, description="Refresh Token"),
                    'access': openapi.Schema(type=openapi.TYPE_STRING, description="Access Token"),
                }
            )
        )}
    )
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            try:
                user = AdminUser.objects.get(email=email)
                if user.check_password(password):
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Incorrect password"}, status=status.HTTP_401_UNAUTHORIZED)
            except AdminUser.DoesNotExist:
                return Response({"error": "Admin user not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Manage Users
class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

# Manage Quizzes
class AdminQuizListView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminQuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAdminUser]

# Manage Questions
class AdminQuestionListView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminQuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAdminUser]
