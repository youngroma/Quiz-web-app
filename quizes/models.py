from django.db import models
import random

DIFF_CHOICES = (
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
)


class Quiz(models.Model):
    title = models.CharField(max_length=255, help_text="Title of the quiz", blank=True)
    description = models.TextField(help_text="Description of the quiz", blank=True, null=True)
    time = models.IntegerField(help_text="Duration of the quiz in minutes")
    required_score = models.DecimalField(help_text="Score needed to pass the quiz in %", decimal_places=2, max_digits=6)
    difficulty = models.CharField(max_length=6, choices=DIFF_CHOICES, help_text="Difficulty level of the quiz")

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def get_questions(self):
        return self.questions.all()

    class Meta:
        verbose_name_plural = 'Quizes'

