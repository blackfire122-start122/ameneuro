from django import forms
from django.contrib.auth.forms import (UserCreationForm,
								AuthenticationForm,
								UserChangeForm,
								PasswordResetForm)
from django.forms import(ModelForm, 
						TextInput,
						PasswordInput, 
						FileInput,
						ModelMultipleChoiceField, 
						Select,
						FileField,
						IntegerField,
						ModelChoiceField)
from .models import User

class RegisterForm(UserCreationForm):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['username'].widget = TextInput(attrs={
				'class':'form_name','placeholder':'username'})
		self.fields['password1'].widget = PasswordInput(attrs={
				'class':'form_pass','placeholder':'pass1'})
		self.fields['password2'].widget = PasswordInput(attrs={
				'class':'form_pass','placeholder':'pass2'})

	class Meta:
		model = User
		fields = ['username','password1','password2']

class LoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].widget = TextInput(attrs={
				'class':'form_name',
				'placeholder':'Name',
			})
		self.fields['password'].widget = PasswordInput(attrs={
				'class':'form_pass',
				'placeholder':'pass',
			})
	class Meta:
		model = User
		fields = ['username','password']