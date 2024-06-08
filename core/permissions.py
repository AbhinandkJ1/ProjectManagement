from django.apps import AppConfig
from django.contrib.auth.models import Group
from rest_framework import permissions

class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        admin_group, created = Group.objects.get_or_create(name='admin')
        manager_group, created = Group.objects.get_or_create(name='manager')
        member_group, created = Group.objects.get_or_create(name='member')



class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='admin').exists()

class ManagerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='manager').exists()

class MemberPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='member').exists()
