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
from .models import User, Post, TypeFile, Theme, Music, Message, AllTheme, TypeMes, Playlist, Video, ComplainPost
from emoji_picker.widgets import EmojiPickerTextInputAdmin, EmojiPickerTextareaAdmin
from django.conf import settings
import magic

class RegisterForm(UserCreationForm):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['username'].widget = TextInput(attrs={
				'class':'input','placeholder':''})
		self.fields['password1'].widget = PasswordInput(attrs={
				'class':'input','placeholder':''})
		self.fields['password2'].widget = PasswordInput(attrs={
				'class':'input','placeholder':''})
		self.fields['email'].widget = TextInput(attrs={
				'class':'input','placeholder':''})
	class Meta:
		model = User
		fields = ['username','password1','password2','email']

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
		for i in TypeFile.objects.all():
			if i.type_f_magic in type_f:
				post.type_p = i
				break
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

	def save(self):
		mes = ModelForm.save(self)
		if not mes.file:
			return mes
			
		type_f = magic.from_buffer(open(str(settings.MEDIA_ROOT)+str(mes.file),"rb").read(2048))
		for i in TypeFile.objects.all():
			if i.type_f_magic in type_f:
				mes.type_file = i
				break
		mes.save()
		
		return mes

class MessageVoiceForm(ModelForm):
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
				"save_img",
				"add_img",
				"chats_img",
				"find_img",
				"friends_img",
				"activity_img",
				"menu_img",
				"settings_img",
				"play_in_all_img",
				"no_media_img",
				"file_send_img",
				"options_img",
				"pause_img",
				"play_img",
				"music_share_img",
				"end_scroll_img",
				"music_left_img",
				"music_right_img",
				"close_img",
				"turn_over_img",
		]+fields_text
		
		widgets = {i:TextInput(attrs={'class':'form_name_change','placeholder':i}) for i in fields_text}

class PlaylistForm(ModelForm):
	class Meta:
		model = Playlist
		fields = ["name","img","autor"]

class VideoForm(ModelForm):
	class Meta:
		model = Video
		fields = ["name","file","description","preview"]

	def save(self,user):
		video = ModelForm.save(self)
		video.user_pub = user
		video.save()

class ComplainPostForm(ModelForm):
	class Meta:
		model = ComplainPost
		fields = ["theme","description","autor"]