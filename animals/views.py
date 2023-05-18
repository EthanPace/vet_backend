from django.http import JsonResponse
from .models import Animal
from .serializers import AnimalSerializer
from json import loads, dumps

def show(request, id):
	animal = Animal.objects.get(id=id)
	return JsonResponse(animal, safe=False)

def create(request):
	animal = loads(request.body)
	serializer = AnimalSerializer(data=animal)
	if serializer.is_valid():
		serializer.save()
		return JsonResponse(serializer.data, safe=False)
	return JsonResponse(serializer.errors, safe=False)

def update(request, id):
	animal = Animal.objects.get(id=id)
	updated_animal = loads(request.body)
	serializer = AnimalSerializer(animal, data=updated_animal)
	if serializer.is_valid():
		serializer.save()
		return JsonResponse(serializer.data, safe=False)
	return JsonResponse(serializer.errors, safe=False)

def delete(request, id):
	animal = Animal.objects.get(id=id)
	animal.delete()
	return JsonResponse("Deleted animal with id: " + str(id), safe=False)
