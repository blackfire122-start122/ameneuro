from django.db import models
from django.contrib.auth.models import AbstractUser

class Comment(models.Model):
	user = models.ForeignKey("User", on_delete=models.CASCADE)
	parent = models.ForeignKey("self",on_delete=models.CASCADE,null=True,blank=True)
	text = models.TextField()

	def __str__(self):
		return self.text

class Post(models.Model):
	user_pub = models.ForeignKey("User", on_delete=models.CASCADE,null=True)
	type_p = models.CharField(max_length=15,null=True)
	file = models.FileField(upload_to='posts')
	likes = models.IntegerField()
	description = models.TextField(blank=True,null=True)
	comments = models.ManyToManyField("Comment",null=True,blank=True)
	
	def __str__(self):
		return self.file.url

class Message(models.Model):
	text = models.TextField() 
	file = models.FileField(upload_to='message_file',null=True,blank=True)

	def __str__(self):
		return self.text

class Chat(models.Model):
	friend = models.ForeignKey("User", on_delete=models.CASCADE)
	messages = models.ManyToManyField("Message",null=True)
	chat_id = models.CharField(max_length=255,null=True, blank=False)
	def __str__(self):
		return self.chat_id
class User(AbstractUser):
	img = models.ImageField(upload_to='user_img', null=True, blank=True)
	friends = models.ManyToManyField("User",symmetrical=False,null=True,blank=True)
	chats = models.ManyToManyField("Chat",symmetrical=False,null=True,blank=True)

	def __str__(self):
		return self.username

	class Meta:
		verbose_name = "User"
		verbose_name_plural = "Users"
	pass