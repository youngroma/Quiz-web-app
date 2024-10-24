from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.utils import json
from quizes.models import Quiz
from questions.models import Question, Answer

class QuizAPITestCase(APITestCase):
    def test_get_quiz(self):
        # Create test quiz
        quiz = Quiz.objects.create(
            title="Test Quiz",
            description="Test Description",
            time=30,
            required_score=75.00,
            difficulty="easy"
        )

        # Create quiz question and answers
        question = Question.objects.create(quiz=quiz, question_text="Test Question")
        Answer.objects.create(question=question, answer_text="Answer 1", is_correct=True)
        Answer.objects.create(question=question, answer_text="Answer 2", is_correct=False)

        response = self.client.get(reverse('quizes:quiz-data-view', args=[quiz.pk]))

        self.assertEqual(response.status_code, 200)

        # Uploading data from response
        response_data = json.loads(response.content)

        self.assertEqual(len(response_data['data']), 1)
        self.assertIn('Test Question', response_data['data'][0])

        # Check that the question has two answers
        self.assertEqual(len(response_data['data'][0]['Test Question']), 2)









