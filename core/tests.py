from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Project
from .views import ProjectView
from .serializers import *
from .models import *
from rest_framework.authtoken.models import Token
from datetime import date

class ProjectModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.project_owner = ProjectUser.objects.create(user=self.user, role='admin')

    def test_project_creation(self):
        project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            project_owner=self.project_owner
        )
        self.assertEqual(project.name, 'Test Project')
        self.assertEqual(project.description, 'Test Description')
        self.assertEqual(project.project_owner, self.project_owner)


class TaskModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password123')
        cls.project_owner = ProjectUser.objects.create(user=cls.user, role='admin')
        cls.project = Project.objects.create(
        name='Test Project',
        description='Test Description',
        project_owner=cls.project_owner  
    )
        
    def setUp(self):
        self.task = Task.objects.create(
            project=self.project,
            name='Test Task',
            description='Test Description',
            assigned_to=self.user
        )

    def test_task_creation(self):
        self.assertEqual(self.task.project, self.project)
        self.assertEqual(self.task.name, 'Test Task')
        self.assertEqual(self.task.description, 'Test Description')
        self.assertEqual(self.task.assigned_to, self.user)

class MilestoneModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password123')
        cls.project_owner = ProjectUser.objects.create(user=cls.user, role='admin')
        cls.project = Project.objects.create(name='Test Project', description='Test Description', project_owner=cls.project_owner)
        
    def setUp(self):
        self.milestone = Milestone.objects.create(
            project=self.project,
            name='Test Milestone',
            due_date=date(2024, 6, 15) 
        )

    def test_milestone_creation(self):
        self.assertEqual(self.milestone.project, self.project)
        self.assertEqual(self.milestone.name, 'Test Milestone')
        self.assertEqual(self.milestone.due_date, date(2024, 6, 15))

class ProjectSerializerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.project_owner = ProjectUser.objects.create(user=self.user, role='admin')
        self.project = Project.objects.create(name='Test Project', description='Test Description', project_owner=self.project_owner)

    def test_project_serialization(self):
        serializer = ProjectSerializer(self.project)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'id', 'name', 'description', 'project_owner'})
        self.assertEqual(data['name'], self.project.name)
        self.assertEqual(data['description'], self.project.description)
        self.assertEqual(data['project_owner'], self.project_owner.id)

    def test_project_deserialization(self):
        data = {'name': 'New Project', 'description': 'New Description', 'project_owner': self.project_owner.id}
        serializer = ProjectSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        project = serializer.save()
        self.assertEqual(project.name, 'New Project')
        self.assertEqual(project.description, 'New Description')
        self.assertEqual(project.project_owner, self.project_owner)


class TaskSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.project_owner = ProjectUser.objects.create(user=self.user, role='admin')
        self.project = Project.objects.create(name='Test Project', description='Test Description', project_owner=self.project_owner)
        self.task = Task.objects.create(project=self.project, name='Test Task', description='Test Task Description', assigned_to=self.user)

    def test_task_serialization(self):
        serializer = TaskSerializer(self.task)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'id', 'project', 'name', 'description', 'assigned_to'})
        self.assertEqual(data['project'], self.project.id)
        self.assertEqual(data['name'], self.task.name)
        self.assertEqual(data['description'], self.task.description)
        self.assertEqual(data['assigned_to'], self.user.id)

    def test_task_deserialization(self):
        data = {'project': self.project.id, 'name': 'New Task', 'description': 'New Task Description', 'assigned_to': self.user.id}
        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        task = serializer.save()
        self.assertEqual(task.project, self.project)
        self.assertEqual(task.name, 'New Task')
        self.assertEqual(task.description, 'New Task Description')
        self.assertEqual(task.assigned_to, self.user)
    

class MilestoneSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.project_owner = ProjectUser.objects.create(user=self.user, role='admin')
        self.project = Project.objects.create(name='Test Project', description='Test Description', project_owner=self.project_owner)
        self.milestone = Milestone.objects.create(project=self.project, name='Test Milestone', due_date=date(2024, 6, 15))

    def test_milestone_serialization(self):
        serializer = MilestoneSerializer(self.milestone)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'id', 'project', 'name', 'due_date'})
        self.assertEqual(data['project'], self.project.id)
        self.assertEqual(data['name'], self.milestone.name)
        self.assertEqual(data['due_date'], '2024-06-15')

    def test_milestone_deserialization(self):
        data = {'project': self.project.id, 'name': 'New Milestone', 'due_date': '2024-06-20'}
        serializer = MilestoneSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        milestone = serializer.save()
        self.assertEqual(milestone.project, self.project)
        self.assertEqual(milestone.name, 'New Milestone')
        self.assertEqual(milestone.due_date, date(2024, 6, 20))