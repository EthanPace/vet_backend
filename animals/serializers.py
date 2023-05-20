from rest_framework import serializers
from .models import Animal

class AnimalSerializer(serializers.ModelSerializer):
	class Meta:
		model = Animal
		fields = ['id', 'owner', 'name', 'species', 'breed', 'colour', 'sex', 'DOB', 'weight', 'vaccination_status', 'last_vaccination_date', 'next_vaccination_date', 'desexed', 'microchip_number']
