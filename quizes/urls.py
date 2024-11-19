from django.urls import path
from quizes import views
from .views import (
    QuizListView,
    quiz_view,
    quiz_data_view,
    save_quiz_view,
    create_quiz_view,
    create_question_view,
    quiz_results_view,
    logout_user,

)
from django.contrib.auth import views as auth_views

app_name = 'quizes'

urlpatterns = [
    path('', QuizListView.as_view(), name='main-view'),
    path('add_quiz/', create_quiz_view.as_view(), name='add-quiz-view'),
    path('add_questions/<str:pk>/', create_question_view.as_view(), name='add-question-view'),
    path('quiz/<pk>/', quiz_view, name='quiz-view'),
    path('quiz/<pk>/save/', save_quiz_view, name='save-view'),
    path('quiz/<pk>/data/', quiz_data_view, name='quiz-data-view'),
    path('quiz/<pk>/results/', quiz_results_view, name='quiz-results'),
    path('login/', auth_views.LoginView.as_view(template_name='quizes/login.html'), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', views.register, name='register'),

]
