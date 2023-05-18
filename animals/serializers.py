from rest_framework import serializers
from .models import Animal

class AnimalSerializer(serializers.ModelSerializer):
	class Meta:
		model = Animal
		#fields = ['id', 'name', 'species', 'breed', 'age', 'colour', 'weight', 'description', 'image_url', 'created_at', 'updated_at']
		fields = ['id', 'name', 'age', 'breed', 'species', 'colour', 'weight', 'DOB', 'vaccination_status', 'microchip_number', 'owner', 'created_at']