from django.db import models

class Owner(models.Model):
	id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	phone_number = models.CharField(max_length=255)
	available_times = models.CharField(max_length=255)
	def __to_lib__():
		return {
			"id": self.id,
			"first_name": self.first_name,
			"last_name": self.last_name,
			"email": self.email,
			"phone_number": self.phone_number,
			"available_times": self.available_times,
		}