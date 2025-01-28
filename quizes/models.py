from django.db import models
import random

DIFF_CHOICES = (
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
)


class Quiz(models.Model):
    title = models.CharField(max_length=64, blank=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    time = models.IntegerField()
    required_score = models.DecimalField(decimal_places=2, max_digits=6)
    difficulty = models.CharField(max_length=6, choices=DIFF_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def get_questions(self):
        return self.questions.all()

    class Meta:
        verbose_name_plural = 'Quizes'

