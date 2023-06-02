from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Owner
from .serializers import OwnerSerializer
from json import loads
from animals.models import Animal
# Index
# Takes no arguments
# Returns an overview of all owners
def index(request):
	# check if the request method is GET
	if request.method == 'GET':
		# check if the user is logged in
		if request.session.get('logged_in', False) == True:
			# check if the page and page_size parameters are in the request
			if 'page' in request.GET:
				# get the page and page_size parameters from the request
				page = int(request.GET.get('page', 1))
				page_size = int(request.GET.get('page_size', 10))
				# get the owners for the given page
				owners = Owner.objects.all()[(page - 1) * page_size:page * page_size]
			else:
				# get all owners
				owners = Owner.objects.all()
			# serialize the owners
			serializer = OwnerSerializer(owners, many=True)
			# return the overview of the full list of owners
			return JsonResponse(overview(serializer.data), safe=False, status=200)
		else:
			# return an error if the user is not logged in
			return JsonResponse({'error': 'You must be logged in to view this page.'}, status=401)
	else:
		# return an error if the request method is not GET
		return JsonResponse({'error': 'This endpoint only accepts GET requests.'}, status=405)
# Details
# Takes an id as part of the endpoint
# Returns the full details of the owner with the given id
def details(request, id):
	# check if the request method is GET
	if request.method == 'GET':
		# check if the user is logged in
		if request.session.get('logged_in', False) == True:
			# find the owner with the given id
			owner = Owner.objects.filter(id=id)
			# check if the owner exists
			if owner:
				# serialize the owner (not entirely sure why this is necessary)
				serializer = OwnerSerializer(owner[0])
				# return the serialized owner data
				return JsonResponse(find_pets(serializer.data), safe=False, status=200)
			else:
				# return an error if the owner doesn't exist
				return JsonResponse({'error': 'No owner found with that id.'}, status=400)
		else:
			# return an error if the user is not logged in
			return JsonResponse({'error': 'You must be logged in to view this page.'}, status=401)
	else:
		# return an error if the request method is not GET
		return JsonResponse({'error': 'This endpoint only accepts GET requests.'}, status=405)
# Add
# Create functionality for owners
# Takes all owner fields as part of the request body
# Returns the full details of the newly created owner
@csrf_exempt
def add(request):
	# check if the request method is POST
	if request.method == 'POST':
		# check if the user is logged in as an admin
		if request.session.get('user_role', None) == "admin":
			# get the request body and load as json
			body = request.body.decode('utf-8')
			data = loads(body)
			# create a new owner with the given data
			serial = OwnerSerializer(data=data)
			# check if the data is valid
			if serial.is_valid():
				# save the new owner
				serial.save()
				# return a success message with the new owner data
				return JsonResponse({"result":"success", "id":serial.data["id"]}, safe=False, status=201)
			else:
				# return an error if the data is invalid
				return JsonResponse({'error': 'Invalid data.', 'messages':serial.error_messages}, status=400)
		else:
			# return an error if the user is not logged in as an admin
			return JsonResponse({'error': 'You must be logged in as an admin to view this page.'}, status=401)
	else:
		# return an error if the request method is not POST
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'}, status=405)
# Edit
# Update functionality for owners
# Takes an id as part of the endpoint and all owner fields as part of the request body
# Returns the id of the updated owner
@csrf_exempt
def edit(request, id):
	# check if the request method is PUT
	if request.method == 'PUT':
		# check if the user is logged in as an admin
		if request.session.get('user_role', None) == "admin":
			# get the request body and load as json
			data = loads(request.body)
			# find the owner with the given id
			owner = Owner.objects.filter(id=id)
			# check if the owner exists
			if owner:
				# serialize the owner
				serial = OwnerSerializer(data=data)
				# check if the data is valid
				if serial.is_valid():
					# update the owner with the given data
					owner.update(**serial.validated_data)
				else:
					# return an error if the data is invalid
					return JsonResponse({'error': 'Invalid data.', 'messages':serial.error_messages}, status=400)
				# return a success message with the updated owner id
				return JsonResponse({"result":"success",'id': owner[0].id}, safe=False, status=200)
			else:
				# return an error if the owner doesn't exist
				return JsonResponse({'error': 'No owner found with that id.'}, status=400)
		else:
			# return an error if the user is not logged in as an admin
			return JsonResponse({'error': 'You must be logged in as an admin to view this page.'}, status=401)
	else:
		# return an error if the request method is not PUT
		return JsonResponse({'error': 'This endpoint only accepts PUT requests.'}, status=405)
# Delete
# Delete functionality for owners
# Takes an id as part of the endpoint
# Returns a success/fail message
@csrf_exempt
def delete(request, id):
	# check if the request method is DELETE
	if request.method == 'DELETE':
		# check if the user is logged in as an admin
		if request.session.get('user_role', None) == "admin":
			# find the owner with the given id
			owner = Owner.objects.filter(id=id)
			# check if the owner exists
			if owner:
				# delete the owner
				owner.delete()
				# return a success message
				return JsonResponse({'success': 'Owner deleted successfully.'}, status=200)
			else:
				# return an error if the owner doesn't exist
				return JsonResponse({'error': 'No owner found with that id.'}, status=400)
		else:
			# return an error if the user is not logged in as an admin
			return JsonResponse({'error': 'You must be logged in as an admin to view this page.'}, status=401)
	else:
		# return an error if the request method is not DELETE
		return JsonResponse({'error': 'This endpoint only accepts DELETE requests.'}, status=405)
# Overview
# Takes a list of owners
# Returns an summarised view of the owners
# TODO: Check with Maclane to see if this is what he wants
def overview(data):
	# create an empty list to store the overview data
	overview = []
	# iterate over the owners
	for datum in data:
		# append the owner id, first name, last name, and email to the overview list
		overview.append({
			'id': datum['id'],
			'first_name': datum['first_name'],
			'last_name': datum['last_name'],
			'email': datum['email'],
		})
	# return the overview
	return overview
# Find Pets
# Takes an owner
# Returns the owner with an embedded list of their pets
def find_pets(owner):
	# find the pets belonging to the owner
	pets = Animal.objects.filter(owner=owner['id'])
	# create an empty list to store the pets
	owner['pets'] = []
	# iterate over the pets
	for pet in pets:
		# append the pet id, name, and species to the pet list
		owner['pets'].append({
			'id': pet.id,
			'name': pet.name,
			'species': pet.species,
		})
	# return the owner with the embedded pets
	return owner