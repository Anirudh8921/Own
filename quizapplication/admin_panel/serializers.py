from rest_framework import serializers
from .models import AdminUser
from quiz.models import User, Quiz, Question

class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ["id", "email", "is_active"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "is_active"]

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
        ref_name = 'AdminQuizSerializer'  # Different ref_name to avoid conflicts

# In admin_panel/serializers.py
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        ref_name = 'AdminQuestionSerializer'  # Add this to prevent Swagger conflict


