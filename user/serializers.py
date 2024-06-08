from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import ProjectUser, ROLE_CHOICES

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ProjectUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    role = serializers.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = ProjectUser
        fields = ['username', 'password', 'email', 'role']

    def create(self, validated_data):
        # Extract user data
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create project user
        project_user = ProjectUser.objects.create(user=user, **validated_data)
        return project_user