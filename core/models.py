from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser, User


ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('member', 'Member'),
    ]


class ProjectUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default='member')

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Add user to the appropriate group based on the role
        group, created = Group.objects.get_or_create(name=self.role)
        self.user.groups.add(group)


class Project(models.Model):
    name = models.CharField(max_length=40,null=True,blank=True)
    description = models.TextField(blank=True,null=True,max_length=200)
    project_owner = models.ForeignKey(ProjectUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    
class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField(max_length=200,null=True,blank=True)
    assigned_to = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.project


class Milestone(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True,blank=True)
    due_date = models.DateField()

    def __str__(self):
        return self.project


class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField(max_length=200,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user