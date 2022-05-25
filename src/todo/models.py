from django.db import models
from django.contrib.auth.models import User


class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    finished = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
