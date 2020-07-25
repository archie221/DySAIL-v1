from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	first_name = forms.CharField()
	last_name = forms.CharField(required=False)

	class Meta:
		model = User
		fields = ['username','first_name','last_name', 'email', 'password1', 'password2']
		labels = {'username':'Roll No'}
		help_texts = {'username':'Required Format, For eg:18CS10006'}

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email'] 
		labels = {'username':'Roll No'}
		help_texts = {'username':'Required Format, For eg:18CS10006'}