from django.db import models

class Animal(models.Model):
	id = models.AutoField(primary_key=True)

	owner = models.ForeignKey('owners.Owner', on_delete=models.CASCADE)

	name = models.CharField(max_length=50)
	species = models.CharField(max_length=50)
	breed = models.CharField(max_length=50)
	colour = models.CharField(max_length=50)
	sex = models.CharField(max_length=50)
	DOB = models.DateField()
	weight = models.IntegerField()

	vaccination_status = models.CharField(max_length=255)
	last_vaccination_date = models.DateField()
	next_vaccination_date = models.DateField()

	desexed = models.BooleanField()
	deceased = models.BooleanField()

	microchip_number = models.IntegerField()

	def __str__(self):
		return self.name
