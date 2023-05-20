from django.db import models

class Owner(models.Model):
	id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	phone_number = models.IntegerField()
	email = models.EmailField()
	address = models.CharField(max_length=50)
	availability = models.CharField(max_length=255)

	staff = models.BooleanField(default=False)
    
	def __str__(self):
		return self.first_name + " " + self.last_name