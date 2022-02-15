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
from .models import User, Post, TypeFile, Theme, Music, Message, AllTheme, TypeMes
from django.conf import settings
import magic

imgs = ["JPEG image data","PNG image data"]
videos = ["ISO Media"]
audios = ["Audio file"]

ImgObj = TypeFile.objects.get(type_f='img')
VideoObj = TypeFile.objects.get(type_f='video')
AudioObj = TypeFile.objects.get(type_f='audio')

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

class PostForm(ModelForm):
	file = FileInput()
	description = TextInput()

	class Meta:
		model = Post
		fields = ['description', 'file']

	def save(self,user):
		post = ModelForm.save(self)
		post.user_pub = user

		type_f = magic.from_buffer(open(str(settings.MEDIA_ROOT)+str(post.file),"rb").read(2048))

		if any(([i in type_f for i in imgs])):post.type_p = ImgObj
		elif any(([i in type_f for i in videos])):post.type_p = VideoObj
		elif any(([i in type_f for i in audios])):post.type_p = AudioObj

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
	class Meta:
		model = Theme
		fields = ['color_mes_bg_op','color_mes','color_mes_bg','background','name']

class MusicForm(ModelForm):
	class Meta:
		model = Music
		fields = ["name","file"]

class MessageForm(ModelForm):
	class Meta:
		model = Message
		fields = ["file","text"]

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
				"back_img",
				"music_img",
		]+fields_text
		
		widgets = {i:TextInput(attrs={'class':'form_name_change','placeholder':i}) for i in fields_text}
		