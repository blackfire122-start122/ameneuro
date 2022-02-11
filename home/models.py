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
	def __str__(self):
		return self.type_f

class Post(models.Model):
	user_pub = models.ForeignKey("User", on_delete=models.CASCADE,null=True,related_name="user_pub_post")
	type_p = models.ForeignKey("TypeFile", on_delete=models.CASCADE,related_name="type_file_post",null=True)
	date = models.DateField(auto_now=True)
	file = models.FileField(upload_to='posts')
	likes = models.ManyToManyField("User", null=True,blank=True, related_name="likes_post")
	description = models.TextField(blank=True,null=True)
	comments = models.ManyToManyField("Comment",null=True,blank=True)
	
	def __str__(self):
		return self.file.url

class Theme(models.Model):
	color_mes = models.CharField(max_length=15,null=True)
	color_mes_bg = models.CharField(max_length=15,null=True)
	background = models.FileField(upload_to='themes',default='themes/default.jpg',null=True,blank=False)

	name = models.CharField(max_length=100,null=True)

	def __str__(self):
		return self.name

class TypeMes(models.Model):
	type_m = models.CharField(max_length=15)
	def __str__(self):
		return self.type_m

class Message(models.Model):
	user = models.ForeignKey("User", on_delete=models.CASCADE,null=True)
	type_m = models.ForeignKey("TypeMes",on_delete=models.CASCADE,related_name="type_mes",null=True,blank=True)
	text = models.TextField(null=True,blank=True) 
	file = models.FileField(upload_to='message_file',null=True,blank=True)
	type_file = models.ForeignKey("TypeFile", on_delete=models.CASCADE,related_name="type_file_mes",null=True)
	date = models.DateTimeField(null=True,auto_now=True)
	readeble = models.BooleanField(null=True,default=False)
	def __str__(self):
		return self.text

class Chat(models.Model):
	users = models.ManyToManyField("User",null=True, related_name="user_chat")
	messages = models.ManyToManyField("Message",null=True)
	theme = models.ForeignKey("Theme",null=True,on_delete=models.CASCADE)
	chat_id = models.CharField(max_length=255,null=True, blank=False)

	def __str__(self):
		return self.chat_id

class Music(models.Model):
	file = models.FileField(upload_to='music',null=False,blank=False)
	name = models.CharField(max_length=15)
	def __str__(self):
		return self.name

class AllTheme(models.Model):
	name = models.CharField(max_length=100,null=True)
	fon_color = RGBColorField(null=True)
	text_color = RGBColorField(null=True)
	header_bg_color = RGBColorField(null=True)
	header_bg_opacity = models.FloatField(null=True,default=1,validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])

	fon_img = models.ImageField(upload_to="theme_all/fon_imgs",default=None,null=True,blank=True)
	comment_img = models.ImageField(upload_to="theme_all/comment_imgs",default="theme_all/comment_imgs/comment.png",null=True)
	like_img = models.ImageField(upload_to="theme_all/like_imgs",default="theme_all/like_imgs/like.png",null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "AllTheme"
		verbose_name_plural = "AllThemes"

def def_all_theme():
	try:return AllTheme.objects.get(name="default").id
	except:return None

class User(AbstractUser):
	img = models.ImageField(upload_to='user_img', default='user_img/user.png', null=True, blank=True)
	friends = models.ManyToManyField("User",symmetrical=True,null=True,blank=True,related_name="friends_user")
	music = models.ManyToManyField("Music",symmetrical=False,null=True,blank=True,related_name="music_user")
	chats = models.ManyToManyField("Chat",symmetrical=False,null=True,blank=True,related_name="chats_user")
	themes = models.ManyToManyField("Theme",null=True,blank=True, related_name="themes_user")
	friend_want_add = models.ManyToManyField("User",symmetrical=False,null=True,blank=True,related_name="friend_want_add_user")
	followers = models.ManyToManyField("User",symmetrical=False,null=True,blank=True,related_name="followers_user")
	follow = models.ManyToManyField("User",symmetrical=False,null=True,blank=True,related_name="follow_user")
	theme_all = models.ForeignKey("AllTheme",default=def_all_theme,null=True,blank=True,on_delete=models.CASCADE,related_name="theme_all_user")

	def __str__(self):
		return self.username

	class Meta:
		verbose_name = "User"
		verbose_name_plural = "Users"

@receiver(pre_delete, sender=AllTheme)
def AllTheme_delete(sender, instance, **kwargs):
	try:
		old_instance = AllTheme.objects.get(id=instance.id)
		if old_instance.comment_img != 'theme_all/comment_imgs/comment.png' and old_instance.like_img != 'theme_all/like_imgs/like.png':
			old_instance.comment_img.delete(False)
			old_instance.fon_img.delete(False)
			old_instance.like_img.delete(False)
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
	try:
		instance.file.delete(False)
	except:pass

@receiver(pre_delete, sender=Theme)
def Theme_delete(sender, instance, **kwargs):
	try:
		old_instance = Theme.objects.get(id=instance.id)
		if old_instance.background.url != '/themes/default.jpg':instance.background.delete(False)
	except:pass

@receiver(pre_save, sender=Theme)
def Theme_delete_old(sender, instance, **kwargs):
	try:
		old_instance = Theme.objects.get(id=instance.id)
		if instance.background.url!=old_instance.background.url:old_instance.background.delete(False)
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