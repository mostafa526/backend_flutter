from django.db import models

from accounts.models import User, Role

class FormRequest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    current_level = models.IntegerField(default=1)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class FormApproval(models.Model):
    form = models.ForeignKey(FormRequest, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.IntegerField()
    approved_at = models.DateTimeField(auto_now_add=True)
