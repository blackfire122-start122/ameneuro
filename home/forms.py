from django.contrib.auth.forms import (UserCreationForm,
								AuthenticationForm,
								UserChangeForm,
								PasswordResetForm)
from django.forms import(ModelForm,
						IntegerField, 
						CharField,
						TextInput,
						PasswordInput, 
						FileInput,
						Select,
						FileField)
from .models import User, Post, TypePost

imgs = ["jpg","png"]
videos = ["mp4"]

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

ImgObj = TypePost.objects.get(type_p='img')
VideoObj = TypePost.objects.get(type_p='video')

class PostForm(ModelForm):
	file = FileInput()
	description = TextInput()

	class Meta:
		model = Post
		fields = ['description', 'file']

	def save(self,user):
		post = ModelForm.save(self)
		post.user_pub = user

		if str(post.file)[-3:] in imgs:
			post.type_p = ImgObj
		if str(post.file)[-3:] in videos:
			post.type_p = VideoObj

		post.save()
