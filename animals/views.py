from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Animal
from .serializers import AnimalSerializer
from json import loads
# Index
# Takes no arguments
# Returns an overview of all animals
# TODO: Add pagination
# TODO: Add Authorization
# TODO: Test this
def index(request):
	if request.method == 'GET':
		animals = Animal.objects.all()
		serializer = AnimalSerializer(animals, many=True)
		return overview(serializer.data)
	else:
		return JsonResponse({'error': 'This endpoint only accepts GET requests.'})
# Details
# Takes an id as part of the endpoint
# Returns the full details of the animal with the given id
# TODO: Add Authorization
# TODO: Test this
def details(request, id):
	if request.method == 'GET':
		animal = Animal.objects.filter(id=id)
		if animal:
			serializer = AnimalSerializer(animal[0])
			return JsonResponse(serializer.data, safe=False)
		else:
			return JsonResponse({'error': 'No animal found with that id.'})
	else:
		return JsonResponse({'error': 'This endpoint only accepts GET requests.'})
# Search
# Takes a search term and search text as part of the request body
# Returns a list of animals matching the search term and search text
# TODO: Implement this, add auth, run tests
def search(request):
	return JsonResponse({'error': 'This endpoint is not implemented yet.'})
	if request.method == 'POST':
		data = loads(request.body)
		animals = Animal.objects.filter(name__icontains=data['name'])
		serializer = AnimalSerializer(animals, many=True)
		return JsonResponse(serializer.data, safe=False)
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'})
# Add
# Create functionality for animals
# Takes all animal fields as part of the request body
# Returns the full details of the newly created animal
# TODO: Add Authorization
# TODO: Test this
@csrf_exempt
def add(request):
	if request.method == 'POST':
		body = request.body.decode('utf-8')
		data = loads(body)
		serial = AnimalSerializer(data=data)
		if serial.is_valid():
			serial.save()
			return JsonResponse(serial.data, safe=False)
		else:
			return JsonResponse({'error': 'Invalid data.'})
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'})
# Edit
# Update functionality for animals
# Takes an id as part of the endpoint and all animal fields as part of the request body
# Returns the id of the updated animal
# TODO: Fix the fields on the update line
# TODO: Add Authorization
# TODO: Test this
@csrf_exempt
def edit(request, id):
	if request.method == 'POST':
		data = loads(request.body)
		animal = Animal.objects.filter(id=id)
		if animal:
			animal.update(name=data['name'], age=data['age'], species=data['species'], breed=data['breed'], color=data['color'], weight=data['weight'], height=data['height'], description=data['description'])
			return JsonResponse({'id': animal[0].id})
		else:
			return JsonResponse({'error': 'No animal found with that id.'})
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'})
# Delete
# Delete functionality for animals
# Takes an id as part of the endpoint
# Returns the id of the deleted animal
# TODO: Add Authorization
# TODO: Test this
@csrf_exempt
def delete(request, id):
	if request.method == 'POST':
		animal = Animal.objects.filter(id=id)
		if animal:
			animal.delete()
			return JsonResponse({'success': 'Animal deleted successfully.'})
		else:
			return JsonResponse({'error': 'No animal found with that id.'})
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'})
# Overview
# Takes a list of animals
# Returns an overview of all animals
# TODO: Check with Maclane to see what he needs here
def overview(animals):
	overview = []
	for animal in animals:
		overview.append({
			'id': animal['id'],
			'name': animal['name'],
			'species': animal['species'],
			'breed': animal['breed'],
			'color': animal['color'],
			'weight': animal['weight'],
			'height': animal['height'],
			'description': animal['description']
		})
	return JsonResponse(overview, safe=False)