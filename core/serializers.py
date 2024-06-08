from rest_framework import serializers
from .models import *


class ProjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(allow_blank=False,allow_null=False,max_length=40)
    project_owner = serializers.PrimaryKeyRelatedField(queryset=ProjectUser.objects.all(),required=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'project_owner']

class TaskSerializer(serializers.ModelSerializer):
    project = serializers.CharField(allow_blank=False,allow_null=False)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=True)
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Task
        fields = '__all__'

class MilestoneSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=True)

    class Meta:
        model = Milestone
        fields = '__all__'