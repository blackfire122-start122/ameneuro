from django.db import models
from django.contrib.auth.models import AbstractUser

class Comment(models.Model):
	user = models.ForeignKey("User", on_delete=models.CASCADE,related_name="comment_user")
	parent = models.ForeignKey("self",on_delete=models.CASCADE,null=True,blank=True,related_name="comment_parent")
	text = models.TextField()

	def __str__(self):
		return self.text

class Post(models.Model):
	user_pub = models.ForeignKey("User", on_delete=models.CASCADE,null=True,related_name="user_pub_post")
	type_p = models.CharField(max_length=15,null=True)
	file = models.FileField(upload_to='posts')
	likes = models.ManyToManyField("User", null=True,blank=True, related_name="likes_post")
	description = models.TextField(blank=True,null=True)
	comments = models.ManyToManyField("Comment",null=True,blank=True)
	
	def __str__(self):
		return self.file.url

class Message(models.Model):
	user = models.ForeignKey("User", on_delete=models.CASCADE,null=True)
	text = models.TextField() 
	file = models.FileField(upload_to='message_file',null=True,blank=True)
	date = models.TimeField(null=True,auto_now=True)
	def __str__(self):
		return self.text

class Chat(models.Model):
	users = models.ManyToManyField("User",null=True, related_name="user_chat")
	messages = models.ManyToManyField("Message",null=True)
	chat_id = models.CharField(max_length=255,null=True, blank=False)
	def __str__(self):
		return self.chat_id

class User(AbstractUser):
	img = models.ImageField(upload_to='user_img', null=True, blank=True)
	friends = models.ManyToManyField("User",symmetrical=True,null=True,blank=True,related_name="friends_user")
	chats = models.ManyToManyField("Chat",symmetrical=False,null=True,blank=True,related_name="chats_user")
	friend_want_add = models.ManyToManyField("User",symmetrical=False,null=True,blank=True,related_name="friend_want_add_user")

	def __str__(self):
		return self.username

	class Meta:
		verbose_name = "User"
		verbose_name_plural = "Users"
	pass