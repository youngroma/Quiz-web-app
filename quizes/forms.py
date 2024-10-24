from django import forms
from .models import Quiz
from questions.models import Question, Answer
from django.forms import inlineformset_factory, modelformset_factory
from django.core.exceptions import ValidationError

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'time', 'required_score', 'difficulty']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) > 64:
            raise ValidationError('Quiz title is too long.')
        return title

    def clean_required_score(self):
        required_score = self.cleaned_data.get('required_score')
        if required_score > 100:
            raise ValidationError('Maximum score is 100%.')
        return required_score


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields =  ['question_text', 'question_type']

    def clean_question_text(self):
        text = self.cleaned_data.get('question_text')
        if len(text) > 64:
            raise ValidationError('Question text is too long.')
        return text

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text', 'is_correct']  # id not include
    def clean_answer_text(self):
        text = self.cleaned_data.get('answer_text')
        if len(text) == 0:
            raise ValidationError('Answer text cannot be empty.')
        return text


QuestionFormSet = modelformset_factory(Question, form=QuestionForm, extra=1)
AnswerFormSet = inlineformset_factory(Question, Answer, form=AnswerForm, extra=2, can_delete=True)






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

