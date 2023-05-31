from django.db import models

class Visit(models.Model):
	id = models.AutoField(primary_key=True)
	date_time = models.DateTimeField()
	reason = models.CharField(max_length=255)
	notes = models.CharField(max_length=255)

	animal = models.ForeignKey('animals.Animal', on_delete=models.CASCADE)
    
	def __str__(self):
		return self.date + " " + self.reason