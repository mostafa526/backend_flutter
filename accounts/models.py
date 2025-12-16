from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50)
    level = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name} (Level {self.level})"


class User(AbstractUser):
    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.username