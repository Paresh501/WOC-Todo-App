from django.db import models
from django.conf import settings
from django.utils import timezone

class Task(models.Model):
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    author.is_staff=True
    task_title = models.CharField(max_length=200)
    task_content = models.TextField()
#    to_do_date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.task_title