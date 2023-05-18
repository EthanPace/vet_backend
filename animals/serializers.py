from rest_framework import serializers
from .models import Animal

class AnimalSerializer(serializers.ModelSerializer):
	class Meta:
		model = Animal
		fields = ['id', 'name', 'species', 'breed', 'age', 'color', 'weight', 'description', 'image_url', 'created_at', 'updated_at']