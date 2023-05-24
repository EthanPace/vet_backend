from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Animal
from .serializers import AnimalSerializer
from json import loads
from visits.models import Visit
# Index
# Takes no arguments
# Returns an overview of all animals
# TODO: Add Authorization
# TODO: Test this
def index(request):
	if request.method == 'GET':
		if 'page' in request.GET:
			page = int(request.GET['page', 1])
			page_size = int(request.GET['page_size', 10])
			animals = Animal.objects.all()[(page - 1) * page_size:page * page_size]
		else:
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
			return JsonResponse(find_visits(serializer.data), safe=False)
		else:
			return JsonResponse({'error': 'No animal found with that id.'})
	else:
		return JsonResponse({'error': 'This endpoint only accepts GET requests.'})
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
			animal.update(name=data['name'], species=data['species'], breed=data['breed'], color=data['color'], sex=data['sex'], DOB=data['DOB'], weight=data['weight'], vaccination_status=data['vaccination_status'], last_vaccination_date=data['last_vaccination_date'], next_vaccination_date=data['next_vaccination_date'], desexed=data['desexed'], microchip_number=data['microchip_number'])
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
			"name":animal['name'], 
			"species":animal['species']
		})
	return JsonResponse(overview, safe=False)
# Find Visits
# Takes an animal
# Returns a list of visits for that animal
# TODO: Test this
def find_visits(animal):
	visits = Visit.objects.filter(animal=animal['id'])
	animal['visits'] = visits
	return animal