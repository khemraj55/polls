from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from .models import Poll, Choice
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class PollForm(forms.ModelForm):
    pub_date = forms.DateField(widget=AdminDateWidget)

    class Meta:
        model = Poll
        fields = ['question', 'pub_date', 'end_date']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')