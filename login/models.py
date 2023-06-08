from django.db import models

class User(models.Model):
	id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
	role = models.CharField(max_length=50)
	
	def __str__(self):
		return self.username
	
class AuthToken(models.Model):
	token = models.CharField(max_length=50, unique=True, primary_key=True)
	user_id = models.IntegerField()
	user_role = models.CharField(max_length=50)
	
	def __str__(self):
		return self.token