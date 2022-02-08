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
from .models import User, Post, TypePost, Theme, Music, Message, AllTheme

imgs = ["jpg","png"]
videos = ["mp4"]

class RegisterForm(UserCreationForm):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['username'].widget = TextInput(attrs={
				'class':'input','placeholder':''})
		self.fields['password1'].widget = PasswordInput(attrs={
				'class':'input','placeholder':''})
		self.fields['password2'].widget = PasswordInput(attrs={
				'class':'input','placeholder':''})

	class Meta:
		model = User
		fields = ['username','password1','password2']

class LoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].widget = TextInput(attrs={
				'class':'input',
				'placeholder':' '})
		self.fields['password'].widget = PasswordInput(attrs={
				'class':'input',
				'placeholder':' '})
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

		if str(post.file)[-3:] in imgs:post.type_p = ImgObj
		elif str(post.file)[-3:] in videos:post.type_p = VideoObj

		post.save()

class ChangeForm(UserChangeForm):
	class Meta:
		model = User
		fields = ['username',
			'first_name','last_name',
			'email',
			'img',
			]
		widgets = {
			'username':TextInput(attrs={
				'class':'form_name_change','placeholder':"name",'id':'username'}),
			'first_name':TextInput(attrs={
				'class':'form_name_change','placeholder':'first_name','id':'first_name'}),
			'last_name':TextInput(attrs={
				'class':'form_name_change','placeholder':'last_name','id':'last_name'}),
			'email':TextInput(attrs={
				'class':'form_email_change','placeholder':'Email','id':'email'}),
			}

class ThemeForm(ModelForm):
	mes_bg_op = CharField()
	class Meta:
		model = Theme
		fields = ['color_mes','color_mes_bg','background','mes_bg_op','name']

class MusicForm(ModelForm):
	class Meta:
		model = Music
		fields = ["name","file"]

class MessageForm(ModelForm):
	class Meta:
		model = Message
		fields = ["file","type_m","text"]

class AllThemeForm(ModelForm):
	class Meta:
		model = AllTheme

		fields_text = ["name","header_bg_opacity"]

		fields = ["name",
				"fon_color",
				"text_color",
				"header_bg_color",
				"header_bg_opacity",
				"fon_img",
				"comment_img",
				"like_img",
		]+fields_text
		
		widgets = {i:TextInput(attrs={'class':'form_name_change','placeholder':i}) for i in fields_text}
		