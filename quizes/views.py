from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .forms import QuizForm, AnswerFormSet, QuestionFormSet, QuestionForm
from results.models import Result
from .models import Quiz
from django.views.generic import ListView, CreateView
from django.http import JsonResponse, HttpResponse
from questions.models import Question, Answer
from .utils import DataMixin
from django.shortcuts import render, redirect




# Create your views here.

class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/main.html'


class create_quiz_view(DataMixin, CreateView):
    form_class = QuizForm
    template_name = 'quizes/add_quiz.html'

    def get_success_url(self):
        # Get ID of created viewer
        return reverse_lazy('quizes:add-question-view', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавить вопросы")

        # Get the ID of the viewer from the URL
        pk = self.kwargs.get('pk')
        questions = Question.objects.filter(quiz_id=pk)
        question_formset = QuestionFormSet(prefix='questions', queryset=questions)

        # Add formset to context
        context['question_formset'] = question_formset
        return {**context, **c_def}

class create_question_view(DataMixin, CreateView):
    template_name = 'quizes/add_question.html'
    success_url = reverse_lazy('quizes:main-view')

    def get(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        question_formset = QuestionFormSet(queryset=Question.objects.none(), prefix='questions')  # Empty queryset
        answer_formsets = [AnswerFormSet(queryset=Answer.objects.none(), prefix=f'answers-{i}') for i in range(question_formset.total_form_count())]  # Empty queryset

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
            for question_form, answer_formset in zip(question_formset, answer_formsets):
                question = question_form.save(commit=False)
                question.quiz_id = pk
                question.save()

                for answer_form in answer_formset:
                    answer = answer_form.save(commit=False)
                    answer.question = question  # We link the answer to the question
                    answer.save()

            return redirect(self.success_url)

        # If forms are not valid, return them to the template
        context = {
            'question_formset': question_formset,
            'answer_formsets': answer_formsets,
            'title': "Добавить вопросы"
        }
        return render(request, self.template_name, context)




def quiz_view(request, pk):
    if pk == 'favicon.ico':
        return HttpResponse(status=204)
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

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(question_text=k)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        required_score = quiz.required_score
        score = 0
        multiplier = 100 / len(questions)
        results = []

        for q in questions:
            a_selected = data[q.question_text]

            if a_selected != '':
                correct_answer = Answer.objects.filter(question=q).get(is_correct=True)
                if a_selected == correct_answer.answer_text:
                    score += 1

                results.append({q.question_text: {
                    'correct_answer': correct_answer.answer_text,
                    'answered': a_selected
                }})
            else:
                results.append({q.qustion_text: 'not answered'})

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
