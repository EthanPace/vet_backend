from rest_framework import serializers
from .models import Owner

class OwnerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Owner
		fields = ['id', 'first_name', 'last_name', 'phone_number', 'email', 'address', 'availability', 'staff', 'patients']