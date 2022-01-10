from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
	img = models.ImageField()
	friends = models.ForeignKey('self',on_delete=models.CASCADE,null=True)

	