from django.db import models

# class Note(models.Model):
# 	id = models.AutoField(primary_key=True)
# 	title = models.CharField(max_length=255)
# 	content = models.TextField()
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	owner = models.ForeignKey('owners.Owner', related_name='notes', on_delete=models.CASCADE)
# 	def __repr__(self):
# 		return f"<Note object: {self.title} ({self.id})>"
# 	def __str__(self):
# 		return f"<Note object: {self.title} ({self.id})>"

class Note(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=255)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	owner = models.ForeignKey('owners.Owner', related_name='notes', on_delete=models.CASCADE)

	def __repr__(self):
		return f"<Note object: {self.title} ({self.id})>"

	def __str__(self):
		return f"<Note object: {self.title} ({self.id})>"
