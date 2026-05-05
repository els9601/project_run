from email.policy import default

from django.db import models
from django.contrib.auth.models import User

class Run(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    status = status = models.CharField(
    choices=[
        ('init', 'Init'),
        ('in_progress', 'In progress'),
        ('finished', 'Finished'),
    ],
    default='init')
