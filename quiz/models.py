# quiz/models.py
from django.db import models
from django.contrib.auth.models import User
import random

class Question(models.Model):
    text = models.CharField(max_length=255)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')])

    def save(self, *args, **kwargs):
        if not self.correct_option:
            self.correct_option = random.choice(['a', 'b', 'c', 'd'])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text

class UserResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')])
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.user.username} - {self.question.text} - {self.selected_option}"
