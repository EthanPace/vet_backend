from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Animal
from .serializers import AnimalSerializer
from json import loads
from visits.models import Visit
from owners.models import Owner
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
		return JsonResponse(overview(serializer.data), safe=False, status=200)
	else:
		return JsonResponse({'error': 'This endpoint only accepts GET requests.'}, status=405)
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
			return JsonResponse(find_visits(serializer.data), safe=False, status=200)
		else:
			return JsonResponse({'error': 'No animal found with that id.'}, status=400)
	else:
		return JsonResponse({'error': 'This endpoint only accepts GET requests.'}, status=405)
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
		if find_owner(data['owner']):
			serial = AnimalSerializer(data=data)
			if serial.is_valid():
				serial.save()
				return JsonResponse({"result":"success", "data":serial.data}, safe=False, status=201)
			else:
				return JsonResponse({'error': 'Invalid data.'}, status=400)
		else:
			return JsonResponse({'error': 'No owner found with that id.'}, status=400)
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'}, status=405)
# Edit
# Update functionality for animals
# Takes an id as part of the endpoint and all animal fields as part of the request body
# Returns the id of the updated animal\
# TODO: Add Authorization
# TODO: Test this
@csrf_exempt
def edit(request, id):
	if request.method == 'PUT':
		data = loads(request.body)
		if find_owner(data['owner']):
			animal = Animal.objects.filter(id=id)
			if animal:
				animal.update(
					name=data['name'],
					owner=data['owner'],
					species=data['species'],
					breed=data['breed'],
					color=data['color'],
					sex=data['sex'],
					DOB=data['DOB'],
					weight=data['weight'],
					vaccination_status=data['vaccination_status'],
					last_vaccination_date=data['last_vaccination_date'],
					next_vaccination_date=data['next_vaccination_date'],
					desexed=data['desexed'],
					microchip_number=data['microchip_number'])
				return JsonResponse({"result":"success", 'id': animal[0].id}, safe=False, status=200)
			else:
				return JsonResponse({'error': 'No animal found with that id.'}, status=400)
		else:
			return JsonResponse({'error': 'No owner found with that id.'}, status=400)
	else:
		return JsonResponse({'error': 'This endpoint only accepts PUT requests.'}, status=405)
# Delete
# Delete functionality for animals
# Takes an id as part of the endpoint
# Returns the id of the deleted animal
# TODO: Add Authorization
# TODO: Test this
@csrf_exempt
def delete(request, id):
	if request.method == 'DELETE':
		animal = Animal.objects.filter(id=id)
		if animal:
			animal.delete()
			return JsonResponse({'success': 'Animal deleted successfully.'}, status=200)
		else:
			return JsonResponse({'error': 'No animal found with that id.'}, status=400)
	else:
		return JsonResponse({'error': 'This endpoint only accepts DELETE requests.'}, status=405)
# Overview
# Takes a list of animals
# Returns an overview of all animals
# TODO: Check with Maclane to see what he needs here
def overview(animals):
	overview = []
	for animal in animals:
		overview.append({
			"id":animal['id'],
			"name":animal['name'], 
			"species":animal['species']
		})
	return overview
# Find Visits
# Takes an animal
# Returns a list of visits for that animal
# TODO: Test this
def find_visits(animal):
	visits = Visit.objects.filter(animal=animal['id'])
	animal['visits'] = []
	for visit in visits:
		animal['visits'].append({
			"id":visit.id,
			"date":visit.date,
		})
	return animal
# Find Owner
# Takes an owner id
# Returns the owner with that id
def find_owner(id):
	return Owner.objects.filter(id=id)[0]