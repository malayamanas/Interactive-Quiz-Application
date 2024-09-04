# models.py
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    text = models.CharField(max_length=255)
    is_true = models.BooleanField()

    def __str__(self):
        return self.text

class UserResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.BooleanField(null=True)  # Allow NULL values
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.user.username} - {self.question.text} - {self.selected_answer}"
