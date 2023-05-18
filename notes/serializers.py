from rest_framework import serializers
from .models import Owner

class OwnerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Owner
		fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'available_times']
