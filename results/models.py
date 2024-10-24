from django.db import models
from quizes.models import Quiz
from django.contrib.auth.models import User
# Create your models here.

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="results")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    score = models.DecimalField(max_digits=6, decimal_places=2, help_text="User's score in percentage")
    completed_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Result for Quiz: {self.quiz.title} (User ID: {self.user_id}, Score: {self.score})"
