from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, Milestone
from .tasks import send_task_notification_email

@receiver(post_save, sender=Task)
def task_post_save(sender, instance, created, **kwargs):
    if created:
        subject = f'New Task Created: {instance.name}'
        message = f'A new task has been created in the project {instance.project.name}.'
    else:
        subject = f'Task Updated: {instance.name}'
        message = f'The task in the project {instance.project.name} has been updated.'

    recipient_list = [instance.assigned_to.email]
    send_task_notification_email.delay(subject, message, recipient_list)

@receiver(post_save, sender=Milestone)
def milestone_post_save(sender, instance, created, **kwargs):
    if created:
        subject = f'New Milestone Created: {instance.name}'
        message = f'A new milestone has been created in the project {instance.project.name}.'
    else:
        subject = f'Milestone Updated: {instance.name}'
        message = f'The milestone in the project {instance.project.name} has been updated.'

    recipient_list = [user.email for user in instance.project.project_owner.user_set.all()]
    send_task_notification_email.delay(subject, message, recipient_list)
