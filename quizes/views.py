from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from .forms import QuizForm, AnswerFormSet, QuestionFormSet, QuestionForm
from results.models import Result
from .models import Quiz
from django.views.generic import ListView, CreateView
from django.http import JsonResponse, HttpResponse
from questions.models import Question, Answer, UserAnswer
from .utils import DataMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages



# Create your views here.

class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/main.html'


class create_quiz_view(DataMixin, CreateView):
    form_class = QuizForm
    template_name = 'quizes/add_quiz.html'

    def get_success_url(self):
        return reverse_lazy('quizes:add-question-view', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Add questions")

        pk = self.kwargs.get('pk')
        questions = Question.objects.filter(quiz_id=pk)
        question_formset = QuestionFormSet(prefix='questions', queryset=questions)

        context['question_formset'] = question_formset
        return {**context, **c_def}


class create_question_view(DataMixin, CreateView):
    template_name = 'quizes/add_question.html'
    success_url = reverse_lazy('quizes:main-view')

    def get(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        question_formset = QuestionFormSet(queryset=Question.objects.none(), prefix='questions')
        answer_formsets = [AnswerFormSet(queryset=Answer.objects.none(), prefix=f'answers-{i}') for i in range(question_formset.total_form_count())]

        context = {
            'question_formset': question_formset,
            'answer_formsets': answer_formsets,
            'quiz': quiz,
            'title': "Add questions"
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        question_formset = QuestionFormSet(request.POST, prefix='questions')
        answer_formsets = [AnswerFormSet(request.POST, prefix=f'answers-{i}') for i in range(question_formset.total_form_count())]

        if question_formset.is_valid() and all(af.is_valid() for af in answer_formsets):
            # save only non-empty forms
            for question_form, answer_formset in zip(question_formset, answer_formsets):
                if question_form.cleaned_data and not question_form.cleaned_data.get("DELETE"):
                    question = question_form.save(commit=False)
                    question.quiz_id = pk
                    question.save()

                    #save non-empty forms
                    for answer_form in answer_formset:
                        if answer_form.cleaned_data and not answer_form.cleaned_data.get("DELETE"):
                            answer = answer_form.save(commit=False)
                            answer.question = question  # link the answer to the question
                            answer.save()

            return redirect(self.success_url)

        # If the forms are invalid, we return them in the template
        context = {
            'question_formset': question_formset,
            'answer_formsets': answer_formsets,
            'title': "Add questions"
        }
        return render(request, self.template_name, context)




def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quizes/quiz.html', {'obj': quiz})


def quiz_data_view(request, pk):
    try:
        quiz = Quiz.objects.get(pk=pk)
        questions = []

        # Debug messages
        print(f'Quiz: {quiz.title}, Time: {quiz.time}')

        # Get all questions quiz
        quiz_questions = quiz.questions.all()
        print(f'Questions Count: {quiz_questions.count()}')

        for question in quiz_questions:
            answers = [answer.answer_text for answer in question.answers.all()]
            print(f'Question: {question.question_text}, Answers: {answers}')
            questions.append({str(question.question_text): answers})

        return JsonResponse({
            'data': questions,
            'time': quiz.time
        })
    except Quiz.DoesNotExist:
        return JsonResponse({'error': 'Quiz not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def save_quiz_view(request, pk):
    if request.accepts("application/json"):
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        required_score = quiz.required_score
        score = 0
        multiplier = 100 / len(data_)
        results = []

        result = Result.objects.create(quiz=quiz, user=user, score=0)  # score will be updated later

        for question_text, answer_text in data_.items():
            question = Question.objects.filter(quiz=quiz, question_text=question_text).first()
            correct_answer = Answer.objects.filter(question=question, is_correct=True).first()
            selected_answer = Answer.objects.filter(question=question, answer_text=answer_text[0]).first() if answer_text else None

            # Save user response in UserAnswer
            UserAnswer.objects.create(result=result, question=question, selected_answer=selected_answer)

            if selected_answer and selected_answer == correct_answer:
                score += 1
            results.append({
                'question': question.question_text,
                'answered': selected_answer.answer_text if selected_answer else 'Not answered',
                'correct_answer': correct_answer.answer_text
            })

        final_score = score * multiplier
        result.score = final_score
        result.save()

        json_response = {
            'redirect_url': reverse('quizes:quiz-results', kwargs={'pk': pk}),
            'score': final_score,
            'correct_questions': score,
            'passed': final_score >= required_score,
            'required_score': required_score,
            'results': results
        }
        print(json_response['redirect_url'])
        if final_score >= required_score:
            json_response['passed'] = True
            return JsonResponse(json_response)

        return JsonResponse(json_response)



def quiz_results_view(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)

    results = Result.objects.filter(quiz=quiz, user=request.user)

    # Check if there are results
    if not results.exists():
        return render(request, 'quizes/quiz_results.html', {'error': 'No results found.'})

    # Get the last result
    result = results.last()

    questions = quiz.questions.prefetch_related('answers')

    user_answers = []

    for question in questions:
        try:
            user_answer = UserAnswer.objects.get(result=result, question=question)
            selected_answer = user_answer.selected_answer  # Is the object of the response
        except UserAnswer.DoesNotExist:
            selected_answer = None

        user_answers.append({
            'question_text': question.question_text,
            'answers': question.answers.all(),
            'selected_answer': selected_answer,
            'correct_answer': question.answers.filter(is_correct=True).first(),
        })

    context = {
        'quiz': quiz,
        'score': result.score,
        'user_answers': user_answers,
    }
    return render(request, 'quizes/quiz_results.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Авторизация пользователя после регистрации
            messages.success(request, "You successfully registered.")
            return redirect('quizes:main-view')  # Перенаправление после регистрации
    else:
        form = UserCreationForm()
    return render(request, 'quizes/register.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('quizes:login')

