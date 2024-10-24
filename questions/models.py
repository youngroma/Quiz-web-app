from django.db import models
from quizes.models import Quiz

# Create your models here.
class Question(models.Model):

    QUESTION_TYPE_CHOICES = [
        ('quiz', 'Quiz'),
        ('yes_no', 'Yes or No'),
    ]
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField(help_text="Text of the question", max_length=255, null=True, blank=True)
    question_type = models.CharField(
        max_length=10,
        choices=QUESTION_TYPE_CHOICES,
        default='quiz'
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Question: {self.question_text} (Quiz: {self.quiz.title})"

    def get_answers(self):
        return self.answers.all()    # Relationship with model


class Answer(models.Model):
    answer_text = models.TextField(help_text="Text of the answer", max_length=255, null=True, blank=True)
    is_correct = models.BooleanField(default=False, help_text="Is this answer correct?")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"question {self.question.question_text}, answer: {self.answer_text}, correct: {self.is_correct}"

