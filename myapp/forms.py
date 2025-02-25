
from django import forms

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from myapp.models import Expense

class SighupForm(UserCreationForm):

    class Meta:

        model= User

        fields=["username","password1","email","password2"]

class SighnInForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-5"}))

    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control mb-5"}))

class ExpenseForm(forms.ModelForm):

    class Meta:

        model=Expense

        exclude=("created_at","owner")


