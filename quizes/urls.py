from django.urls import path
from .views import (
    QuizListView,
    quiz_view,
    quiz_data_view,
    save_quiz_view,
    create_quiz_view,
    create_question_view,
    quiz_results_view,

)

app_name = 'quizes'

urlpatterns = [
    path('', QuizListView.as_view(), name='main-view'),
    path('add_quiz/', create_quiz_view.as_view(), name='add-quiz-view'),
    path('add_questions/<int:pk>/', create_question_view.as_view(), name='add-question-view'),
    path('<pk>/', quiz_view, name='quiz-view'),
    path('<pk>/save/', save_quiz_view, name='save-view'),
    path('<pk>/data/', quiz_data_view, name='quiz-data-view'),
    path('<pk>/results/', quiz_results_view, name='quiz-results'),

]
