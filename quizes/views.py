from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import QuizForm, AnswerFormSet, QuestionFormSet, QuestionForm
from results.models import Result
from .models import Quiz
from django.views.generic import ListView, CreateView
from django.http import JsonResponse
from questions.models import Question, Answer
from results.models import Result


# Create your views here.

class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/main.html'


from django.shortcuts import render, redirect
from .forms import QuizForm, QuestionFormSet
from .models import Quiz


def create_quiz_view(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST, prefix='questions')

        if quiz_form.is_valid() and question_formset.is_valid():
            quiz = quiz_form.save()  # Сохраните квиз

            questions = question_formset.save(commit=False)  # Не сохраняйте сразу
            for question in questions:
                question.quiz = quiz  # Связываем вопрос с квизом
                question.save()  # Сохраняем вопрос

                # Здесь вы должны также сохранить ответы, если они существуют
                answers = question_formset.cleaned_data  # Получаем данные ответов
                for answer_data in question_formset.cleaned_data:
                    if answer_data.get('answers'):  # Проверяем, что ответы существуют
                        for answer in answer_data['answers']:
                            if answer.get('text'):  # Проверяем, что текст ответа не пустой
                                Answer.objects.create(
                                    question=question,
                                    text=answer['text'],
                                    is_correct=answer.get('is_correct', False)  # Убедитесь, что поле корректно
                                )

            return redirect('/')  # Перенаправление на главную страницу
        else:
            # Если форма невалидна, отобразите ошибки
            print(quiz_form.errors)  # Отладка: вывод ошибок формы
            print(question_formset.errors)  # Отладка: вывод ошибок формы вопросов
    else:
        quiz_form = QuizForm()
        question_formset = QuestionFormSet(prefix='questions')

    return render(request, 'quizes/add_quiz.html', {
        'quiz_form': quiz_form,
        'question_formset': question_formset,
    })



def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quizes/quiz.html', {'obj': quiz})


def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_guestions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })


def save_quiz_view(request, pk):
    if request.accepts("application/json"):
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        required_score = quiz.required_score
        score = 0
        multiplier = 100 / len(questions)
        results = []

        for q in questions:
            a_selected = data[q.text]

            if a_selected != '':
                correct_answer = Answer.objects.filter(question=q).get(correct=True)
                if a_selected == correct_answer.text:
                    score += 1

                results.append({q.text: {
                    'correct_answer': correct_answer.text,
                    'answered': a_selected
                }})
            else:
                results.append({q.text: 'not answered'})

        final_score = score * multiplier

        Result.objects.create(quiz=quiz, user=user, score=final_score)

        json_response = {
            'score': final_score,
            'correct_questions': score,
            'passed': False,
            'required_score': required_score,
            'results': results
        }

        if final_score >= required_score:
            json_response['passed'] = True
            return JsonResponse(json_response)

        return JsonResponse(json_response)
