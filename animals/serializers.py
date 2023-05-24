from rest_framework import serializers
from .models import Animal

class AnimalSerializer(serializers.ModelSerializer):
	class Meta:
		model = Animal
		fields = ['id', 'owner', 'name', 'species', 'breed', 'colour', 'weight', 'vaccination_status', 'microchip_number']
