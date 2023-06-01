from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import Animal
from .serializers import AnimalSerializer
from json import loads
from visits.models import Visit
from owners.models import Owner
# Index
# Takes no arguments
# Returns an overview of all animals
# TODO: Fix Pagination
def index(request):
	# check if the request method is GET
	if request.method == 'GET':
		# check if the page and page_size parameters are in the request
		if 'page' in request.GET:
			# get the page and page_size parameters from the request
			page = int(request.GET['page', 1])
			page_size = int(request.GET['page_size', 10])
			# get the animals for the given page
			animals = Animal.objects.all()[(page - 1) * page_size:page * page_size]
		else:
			# get all animals
			animals = Animal.objects.all()
		# serialize the animals
		serializer = AnimalSerializer(animals, many=True)
		# return the overview of the full list of animals
		return JsonResponse(overview(serializer.data), safe=False, status=200)
	else:
		# return an error if the request method is not GET
		return JsonResponse({'error': 'This endpoint only accepts GET requests.'}, status=405)
# Details
# Takes an id as part of the endpoint
# Returns the full details of the animal with the given id
def details(request, id):
	# check if the request method is GET
	if request.method == 'GET':
		# find the animal with the given id
		animal = Animal.objects.filter(id=id)
		# check if the animal exists
		if animal:
			# serialize the animal (not entirely sure why this is necessary)
			serializer = AnimalSerializer(animal[0])
			# return the serialized animal data
			return JsonResponse(find_visits(serializer.data), safe=False, status=200)
		else:
			# return an error if the animal doesn't exist
			return JsonResponse({'error': 'No animal found with that id.'}, status=400)
	else:
		# return an error if the request method is not GET
		return JsonResponse({'error': 'This endpoint only accepts GET requests.'}, status=405)
# Add
# Create functionality for animals
# Takes all animal fields as part of the request body
# Returns the full details of the newly created animal
@csrf_exempt
def add(request):
	if request.method == 'POST':
		# get the request body and load as json
		body = request.body.decode('utf-8')
		data = loads(body)
		# check if the owner exists
		if find_owner(data['owner']):
			# convert dates to datetime objects
			data = format(data)
			# serialize the data
			serial = AnimalSerializer(data=data)
			# check if the data is valid
			if serial.is_valid():
				# save the data
				serial.save()
				# return the result
				return JsonResponse({"result":"success", "id":serial.data["id"]}, safe=False, status=201)
			else:
				# return an error if the data is invalid
				return JsonResponse({'error': 'Invalid data.','messages':serial.error_messages}, status=400)
		else:
			# return an error if the owner doesn't exist
			return JsonResponse({'error': 'No owner found with that id.'}, status=400)
	else:
		# return an error if the request method is not POST
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'}, status=405)
# Edit
# Update functionality for animals
# Takes an id as part of the endpoint and all animal fields as part of the request body
# Returns the id of the updated animal
@csrf_exempt
def edit(request, id):
	# check if the request method is PUT
	if request.method == 'PUT':
		# get the request body and load as json
		data = loads(request.body)
		# check if the owner exists
		if find_owner(data['owner']):
			# convert dates to datetime objects
			data = format(data)
			# find the animal with the given id
			animal = Animal.objects.filter(id=id)
			# check if the animal exists
			if animal:
				serial = AnimalSerializer(data=data)
				if serial.is_valid():
					animal.update(**serial.validated_data)
				else:
					# return an error if the data is invalid
					return JsonResponse({'error':'Invalid data.','messages':serial.error_messages}, status=400)
				# return the id of the updated animal with a success message
				return JsonResponse({"result":"success", 'id': animal[0].id}, safe=False, status=200)
			else:
				# return an error if the animal doesn't exist
				return JsonResponse({'error': 'No animal found with that id.'}, status=400)
		else:
			# return an error if the owner doesn't exist
			return JsonResponse({'error': 'No owner found with that id.'}, status=400)
	else:
		# return an error if the request method is not PUT
		return JsonResponse({'error': 'This endpoint only accepts PUT requests.'}, status=405)
# Delete
# Delete functionality for animals
# Takes an id as part of the endpoint
# Returns the id of the deleted animal
@csrf_exempt
def delete(request, id):
	# check if the request method is DELETE
	if request.method == 'DELETE':
		# find the animal with the given id
		animal = Animal.objects.filter(id=id)
		# check if the animal exists
		if animal:
			# delete the animal
			animal.delete()
			# return a success message
			return JsonResponse({'success': 'Animal deleted successfully.'}, status=200)
		else:
			# return an error if the animal doesn't exist
			return JsonResponse({'error': 'No animal found with that id.'}, status=400)
	else:
		# return an error if the request method is not DELETE
		return JsonResponse({'error': 'This endpoint only accepts DELETE requests.'}, status=405)
# Overview
# Takes a list of animals
# Returns an overview of all animals
def overview(animals):
	# create an empty list
	overview = []
	# loop through each animal
	for animal in animals:
		# append the animal's id, name, and species to the list
		overview.append({
			"id":animal['id'],
			"name":animal['name'], 
			"species":animal['species'],
			"breed":animal['breed'],
			"colour":animal['colour'],
		})
	# return the list
	return overview
# Find Visits
# Takes an animal
# Returns a list of visits for that animal
def find_visits(animal):
	# get all visits for the animal
	visits = Visit.objects.filter(animal=animal['id'])
	# create an empty list
	animal['visits'] = []
	# loop through each visit
	for visit in visits:
		# append the visit's id and date_time to the list
		animal['visits'].append({
			"id":visit.id,
			"date_time":visit.date_time,
		})
	# return the animal with the visits added
	return animal
# Find Owner
# Takes an owner id
# Returns the owner with that id
def find_owner(id):
	return Owner.objects.filter(id=id)
# Format
# Takes an animal
# Returns the animal with the dates formatted
def format(animal):
	# check if the animal contains a date of birth
	if animal['DOB']:
		# convert the date of birth to a datetime object
		animal['DOB'] = date(animal['DOB'])
	# check if the animal contains a last vaccination date
	if animal['last_vaccination_date']:
		# convert the last vaccination date to a datetime object
		animal['last_vaccination_date'] = date(animal['last_vaccination_date'])
	# check if the animal contains a next vaccination date
	if animal['next_vaccination_date']:
		# convert the next vaccination date to a datetime object
		animal['next_vaccination_date'] = date(animal['next_vaccination_date'])
	return animal
# Date
# Takes a date string
# Returns a date object
def date(date):
	return datetime.strptime(date, '%Y-%m-%d').date()