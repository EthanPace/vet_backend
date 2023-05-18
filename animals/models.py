from django.db import models

class Animal(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=255)
	age = models.IntegerField()
	breed = models.CharField(max_length=255)
	species = models.CharField(max_length=255)
	colour = models.CharField(max_length=255)
	weight = models.IntegerField()
	DOB = models.DateField()
	vaccination_status = models.CharField(max_length=255)
	microchip_number = models.CharField(max_length=255)
	owner = models.ForeignKey('owners.Owner', related_name='animals', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	def __repr__(self):
		return f"<Animal object: {self.name} ({self.id})>"
	def __str__(self):
		return f"<Animal object: {self.name} ({self.id})>"
