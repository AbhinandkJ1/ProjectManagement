from django.urls import path
from .views import *
urlpatterns=[
    path('project',ProjectView.as_view(),                   name='project-view'),
    path('projectcreate',ProjectCreate.as_view(),           name='projectcreate'),
    path('projectupdate',ProjectUpdate.as_view(),           name='projectupdate'),
    path('projectdelete',ProjectDelete.as_view(),           name='projectdelete'),
    path('taskcreate',TaskCreation.as_view(),               name='taskcreate'),
    path('taskdelete',TaskDeletion.as_view(),               name='taskdelete'),
    path('taskview',TaskView.as_view(),                     name='taskview'),
    path('taskupdate',TaskUpdate.as_view(),                 name='taskupdate'),
    path('milestoneview',MilestoneView.as_view(),           name='milestoneview'),
    path('milestonecreate',MilestoneCreate.as_view(),       name='milestonecreate'),
    path('milestoneupdate',MilestoneUpdate.as_view(),       name='milestoneupdate'),
    path('milestonedelete',MilestoneDelete.as_view(),       name='milestonedelete')

]