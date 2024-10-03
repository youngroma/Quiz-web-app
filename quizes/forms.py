from django import forms
from .models import Quiz
from questions.models import Question, Answer
from django.forms import inlineformset_factory, modelformset_factory
from django.core.exceptions import ValidationError

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'topic', 'number_of_questions', 'time', 'required_score', 'difficulty']

# Форма для создания Question
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

# Формсеты для вопросов, для создания нескольких вопросов
QuestionFormSet = modelformset_factory(Question, form=QuestionForm, extra=1)

# Формсеты для вложенных ответов в каждом вопросе
AnswerFormSet = inlineformset_factory(Question, Answer, fields=['text', 'correct'], extra=3, can_delete=True)


        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-input'}),
        #     'topic': forms.TextInput(attrs={'class': 'form-input'}),
        #     'number_of_questions': forms.IntegerField(attrs={'class': 'form-input'}),
        #     'time': forms.IntegerField(attrs={'class': 'form-input'}),
        #     'required_score': forms.IntegerField(attrs={'class': 'form-input'}),
        #
        # }
    # def clean_title(self):
    #     name = self.cleaned_data['name']
    #     if len(name > 64):
    #         raise ValidationError('This quiz name is longer than the system-defined maximum length')
    #     return name
    #
    # def clean_required_score(self):
    #     required_score = self.cleaned_data['required_score']
    #     if required_score > 101:
    #         raise ValidationError('100% is max value')
    #     return required_score

