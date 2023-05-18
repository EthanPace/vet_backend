from django.db import models

class User(models.Model):
	id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	phone_number = models.CharField(max_length=255)
	available_times = models.CharField(max_length=255)
	def __repr__(self):
		return f"<User object: {self.first_name} ({self.id})>"
	def __str__(self):
		return f"<User object: {self.first_name} ({self.id})>"
