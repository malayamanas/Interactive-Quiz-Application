from django.db import models

# Create your models here.

class Question(models.Model):
    text = models.CharField(max_length=255)
    is_true = models.BooleanField()

    def __str__(self):
        return self.text

class UserResult(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)
