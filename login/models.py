from django.db import models

class User(models.Model):
	id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
