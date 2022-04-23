from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver
from colorful.fields import RGBColorField
from django.core.validators import MaxValueValidator, MinValueValidator

class Comment(models.Model):
	user = models.ForeignKey("User", on_delete=models.CASCADE,related_name="comment_user")
	parent = models.ForeignKey("self",on_delete=models.CASCADE,null=True,blank=True,related_name="comment_parent")
	date = models.DateTimeField(null=True,auto_now=True)
	likes = models.ManyToManyField("User", null=True,blank=True, related_name="likes_comments")
	text = models.TextField()

	def __str__(self):
		return self.text

class TypeFile(models.Model):
	type_f = models.CharField(max_length=15)
	type_f_magic = models.TextField(null=True)
	def __str__(self):
		return self.type_f

class Post(models.Model):
	user_pub = models.ForeignKey("User", on_delete=models.SET_NULL,null=True,related_name="user_pub_post")
	type_p = models.ForeignKey("TypeFile", on_delete=models.SET_NULL,related_name="type_file_post",null=True)
	date = models.DateTimeField(auto_now=True)
	file = models.FileField(upload_to='posts')
	likes = models.ManyToManyField("User", null=True,blank=True, related_name="likes_post")
	description = models.TextField(blank=True,null=True)
	comments = models.ManyToManyField("Comment",null=True,blank=True)
	
	def __str__(self):
		return self.file.url

class Video(models.Model):
	name = models.CharField(max_length=100)
	user_pub = models.ForeignKey("User", on_delete=models.SET_NULL,null=True,related_name="user_pub_video")
	date = models.DateTimeField(auto_now=True)
	file = models.FileField(upload_to='videos')
	likes = models.ManyToManyField("User", null=True,blank=True, related_name="likes_video")
	description = models.TextField(blank=True,null=True)
	comments = models.ManyToManyField("Comment",null=True,blank=True)
	preview = models.ImageField(upload_to="videos_preview",default=None)
	def __str__(self):
		return self.name

class Theme(models.Model):
	color_mes = RGBColorField(null=True)
	color_mes_bg = RGBColorField(null=True)
	color_mes_bg_op = models.FloatField(null=True,default=1,validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
	background = models.FileField(upload_to='themes',default=None,null=True,blank=True)
	name = models.CharField(max_length=100,null=True)

	def __str__(self):
		return self.name

class TypeMes(models.Model):
	type_m = models.CharField(max_length=15)
	def __str__(self):
		return self.type_m

class Message(models.Model):
	user = models.ForeignKey("User", on_delete=models.SET_NULL,null=True)
	type_m = models.ForeignKey("TypeMes",on_delete=models.SET_NULL,related_name="type_mes",null=True,blank=True)
	text = models.TextField(null=True,blank=True) 
	file = models.FileField(upload_to='message_file',null=True,blank=True)
	type_file = models.ForeignKey("TypeFile", on_delete=models.SET_NULL,related_name="type_file_mes",null=True)
	date = models.DateTimeField(null=True,auto_now=True)
	readeble = models.BooleanField(null=True,default=False)
	def __str__(self):
		return self.text

class MessageActivity(models.Model):
	text = models.TextField(null=True,blank=True) 
	from_user = models.ForeignKey("User", on_delete=models.SET_NULL,null=True)
	file = models.FileField(upload_to='message_activity_file',null=True,blank=True)
	type_f = models.ForeignKey("TypeFile", on_delete=models.SET_NULL,related_name="type_file_ma",null=True)
	date = models.DateTimeField(null=True,auto_now=True)
	readeble = models.BooleanField(null=True,default=False)
	def __str__(self):
		return self.text

class Chat(models.Model):
	user = models.ForeignKey("User",null=True, on_delete=models.SET_NULL,related_name="user_chat")
	chat_friend = models.ForeignKey("Chat",null=True, on_delete=models.SET_NULL,related_name="chat_friend_chat")
	messages = models.ManyToManyField("Message",null=True)
	theme = models.ForeignKey("Theme",null=True,on_delete=models.SET_NULL)
	chat_id = models.CharField(max_length=255,null=True, blank=False)

	def __str__(self):
		return self.chat_id

class Music(models.Model):
	file = models.FileField(upload_to='music',null=False,blank=False)
	name = models.CharField(max_length=15)
	def __str__(self):
		return self.name

class AllTheme(models.Model):
	default = models.BooleanField(default=False)
	name = models.CharField(max_length=100,null=True)
	fon_color = RGBColorField(null=True)
	text_color = RGBColorField(null=True)
	header_bg_color = RGBColorField(null=True)
	header_bg_opacity = models.FloatField(null=True,default=1,validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])

	fon_img = models.ImageField(upload_to="theme_all/fon_imgs",default=None,null=True,blank=True)
	comment_img = models.ImageField(upload_to="theme_all/comment_imgs",default=None,null=True,blank=True)
	like_img = models.ImageField(upload_to="theme_all/like_imgs",default=None,null=True,blank=True)
	back_img = models.ImageField(upload_to="theme_all/back_imgs",default=None,null=True,blank=True)
	music_img = models.ImageField(upload_to="theme_all/music_imgs",default=None,null=True,blank=True)
	save_img = models.ImageField(upload_to="theme_all/save_img",default=None,null=True,blank=True)
	add_img = models.ImageField(upload_to="theme_all/add_img",default=None,null=True,blank=True)
	chats_img = models.ImageField(upload_to="theme_all/chats_img",default=None,null=True,blank=True)
	find_img = models.ImageField(upload_to="theme_all/find_img",default=None,null=True,blank=True)
	friends_img = models.ImageField(upload_to="theme_all/friends_img",default=None,null=True,blank=True)
	activity_img = models.ImageField(upload_to="theme_all/activity_img",default=None,null=True,blank=True)
	menu_img = models.ImageField(upload_to="theme_all/menu_img",default=None,null=True,blank=True)
	settings_img = models.ImageField(upload_to="theme_all/settings_img",default=None,null=True,blank=True)
	play_in_all_img = models.ImageField(upload_to="theme_all/play_in_all_img",default=None,null=True,blank=True)
	ai_img = models.ImageField(upload_to="theme_all/ai_img",default=None,null=True,blank=True)
	no_media_img = models.ImageField(upload_to="theme_all/no_media_img",default=None,null=True,blank=True)
	file_send_img = models.ImageField(upload_to="theme_all/file_send_img",default=None,null=True,blank=True)
	options_img = models.ImageField(upload_to="theme_all/options_img",default=None,null=True,blank=True)
	pause_img = models.ImageField(upload_to="theme_all/pause_img",default=None,null=True,blank=True)
	play_img = models.ImageField(upload_to="theme_all/play_img",default=None,null=True,blank=True)
	music_share_img = models.ImageField(upload_to="theme_all/music_share_img",default=None,null=True,blank=True)
	
	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "AllTheme"
		verbose_name_plural = "AllThemes"

def def_all_theme():
	try:
		return AllTheme.objects.get(name="white", default=True).id
	except:return None

class User(AbstractUser):
	img = models.ImageField(upload_to='user_img', default='user_img/user.png', null=True, blank=True)
	friends = models.ManyToManyField("User",symmetrical=True,null=True,blank=True,related_name="friends_user")
	music = models.ManyToManyField("Music",symmetrical=False,null=True,blank=True,related_name="music_user")
	playlists = models.ManyToManyField("Playlist",symmetrical=False,null=True,blank=True,related_name="playlist_user")
	music_shared = models.ManyToManyField("Music",symmetrical=False,null=True,blank=True,related_name="music_shared_user")
	chats = models.ManyToManyField("Chat",symmetrical=False,null=True,blank=True,related_name="chats_user")
	themes = models.ManyToManyField("Theme",null=True,blank=True, related_name="themes_user",symmetrical=False)
	friend_want_add = models.ManyToManyField("User",symmetrical=False,null=True,blank=True,related_name="friend_want_add_user")
	followers = models.ManyToManyField("User",symmetrical=False,null=True,blank=True,related_name="followers_user")
	follow = models.ManyToManyField("User",symmetrical=False,null=True,blank=True,related_name="follow_user")
	theme_all = models.ForeignKey("AllTheme",default=def_all_theme,null=True,blank=True,on_delete=models.SET_DEFAULT,related_name="theme_all_user")
	themes_all = models.ManyToManyField("AllTheme",null=True,blank=True, related_name="themes_all_user")
	saves_posts = models.ManyToManyField("Post",null=True,blank=True, related_name="save_post_user")
	message_activity = models.ManyToManyField("MessageActivity",null=True,blank=True, related_name="message_activity")

	def __str__(self):
		return self.username

	class Meta:
		verbose_name = "User"
		verbose_name_plural = "Users"

class Playlist(models.Model):
	musics = models.ManyToManyField("Music",symmetrical=False,null=True,blank=True,related_name="musics_playlist")
	img = models.ImageField(upload_to="playlists_img",default=None)
	name = models.CharField(max_length=15)
	date = models.DateField(null=True,auto_now=True)
	autor = models.ForeignKey("User", on_delete=models.SET_NULL,null=True,related_name="autor_playlist")
	
	def __str__(self):
		return self.name


@receiver(pre_delete, sender=Playlist)
def Playlist_delete(sender, instance, **kwargs):
	try:instance.img.delete(False)
	except:pass


@receiver(pre_delete, sender=AllTheme)
def AllTheme_delete(sender, instance, **kwargs):
	try:
		old_instance = AllTheme.objects.get(id=instance.id)

		fields = {}
		for i in old_instance.__dict__:
			if i.endswith("img"):fields[i] = True

		for i in AllTheme.objects.filter(default=True):
			for e in fields:
				if i.__dict__.get(e) == old_instance.__dict__.get(e):
					fields[e] = False
		
		for i in fields:
			if fields[i]:
				getattr(old_instance,i).delete(False)
	except:pass

@receiver(pre_save, sender=AllTheme)
def AllTheme_delete_old(sender, instance, **kwargs):
	try:
		if instance.id:
			old_instance = AllTheme.objects.get(id=instance.id)

			fields = {}
			for i in old_instance.__dict__:
				if i.endswith("img"):fields[i] = True

			for i in AllTheme.objects.filter(default=True):
				for e in fields:
					if i.__dict__.get(e) == old_instance.__dict__.get(e):
						fields[e] = False

			for i in fields:
				if old_instance.__dict__.get(i) == instance.__dict__.get(i):
					fields[i] = False

			for i in fields:
				if fields[i]:
					getattr(old_instance,i).delete(False)
	except:pass

@receiver(pre_save, sender=User)
def User_delete_old(sender, instance, **kwargs):
	try:
		old_instance = User.objects.get(id=instance.id)
		if old_instance.img != 'user_img/user.png' and old_instance.img!=instance.img:old_instance.img.delete(False)
	except:pass

@receiver(pre_delete, sender=User)
def User_delete(sender, instance, **kwargs):
	try:
		old_instance = User.objects.get(id=instance.id)
		if old_instance.img.url != '/user_img/user.png':instance.img.delete(False)
	except:pass

@receiver(pre_delete, sender=Post)
def Post_delete(sender, instance, **kwargs):
	try:instance.file.delete(False)
	except:pass

@receiver(pre_delete, sender=Theme)
def Theme_delete(sender, instance, **kwargs):
	try:
		old_instance = Theme.objects.get(id=instance.id)
		instance.background.delete(False)
	except:pass

@receiver(pre_delete, sender=Music)
def Music_delete(sender, instance, **kwargs):
	try:
		instance.file.delete(False)
	except:pass

@receiver(pre_delete, sender=Message)
def Messge_delete(sender, instance, **kwargs):
	try:
		if instance.file.url[:6] != "/posts":
			instance.file.delete(False)
	except:pass

@receiver(pre_delete, sender=Video)
def Video_delete(sender, instance, **kwargs):
	try:
		instance.file.delete(False)
		instance.preview.delete(False)
	except:pass