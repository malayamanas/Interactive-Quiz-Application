# quiz/models.py
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    text = models.CharField(max_length=255)
    option_a = models.CharField(max_length=255, default="N/A")
    option_b = models.CharField(max_length=255, default="N/A")
    option_c = models.CharField(max_length=255, default="N/A")
    option_d = models.CharField(max_length=255, default="N/A")
    correct_option = models.CharField(max_length=1, choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')], null=True, blank=True)
    image = models.ImageField(upload_to='question_images/', null=True, blank=True)

    def __str__(self):
        return self.text

class UserResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')], default='a')
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.user.username} - {self.question.text} - {self.selected_option}"
