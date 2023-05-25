from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Owner
from .serializers import OwnerSerializer
from json import loads
from animals.models import Animal
# Index
# Takes no arguments
# Returns an overview of all owners
# TODO: Add Authorization
# TODO: Test this
def index(request):
	if request.method == 'GET':
		if 'page' in request.GET:
			page = int(request.GET['page', 1])
			page_size = int(request.GET['page_size', 10])
			owners = Owner.objects.all()[(page - 1) * page_size:page * page_size]
		else:
			owners = Owner.objects.all()
		serializer = OwnerSerializer(owners, many=True)
		return JsonResponse(overview(serializer.data), safe=False, status=200)
	else:
		return JsonResponse({'error': 'This endpoint only accepts GET requests.'}, status=405)
# Details
# Takes an id as part of the endpoint
# Returns the full details of the owner with the given id
# TODO: Add Authorization
# TODO: figure out what this does
def details(request, id):
	if request.method == 'GET':
		owner = Owner.objects.filter(id=id)
		if owner:
			serializer = OwnerSerializer(owner[0])
			return JsonResponse(find_pets(serializer.data), safe=False, status=200)
		else:
			return JsonResponse({'error': 'No owner found with that id.'}, status=400)
	else:
		return JsonResponse({'error': 'This endpoint only accepts GET requests.'}, status=405)
# Add
# Create functionality for owners
# Takes all owner fields as part of the request body
# Returns the full details of the newly created owner
# TODO: Add Authorization
# TODO: Make sure this still works
@csrf_exempt
def add(request):
	if request.method == 'POST':
		body = request.body.decode('utf-8')
		data = loads(body)
		serial = OwnerSerializer(data=data)
		if serial.is_valid():
			serial.save()
			return JsonResponse({"result":"success", "data":serial.data}, safe=False, status=201)
		else:
			return JsonResponse({'error': 'Invalid data.'}, status=400)
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'}, status=405)
# Edit
# Update functionality for owners
# Takes an id as part of the endpoint and all owner fields as part of the request body
# Returns the id of the updated owner
# TODO: Add Authorization
# TODO: Test this
@csrf_exempt
def edit(request, id):
	if request.method == 'POST':
		data = loads(request.body)
		owner = Owner.objects.filter(id=id)
		if owner:
			owner.update(
				first_name=data['first_name'],
				last_name=data['last_name'],
				phone_number=data['phone_number'],
				email=data['email'],
				availability=data['availability'],
				staff=data['staff']
			)
			return JsonResponse({"result":"success",'id': owner[0].id}, safe=False, status=200)
		else:
			return JsonResponse({'error': 'No owner found with that id.'}, status=400)
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'}, status=405)
# Delete
# Delete functionality for owners
# Takes an id as part of the endpoint
# Returns a success/fail message
# TODO: Add Authorization
# TODO: Test this
@csrf_exempt
def delete(request, id):
	if request.method == 'POST':
		owner = Owner.objects.filter(id=id)
		if owner:
			owner.delete()
			return JsonResponse({'success': 'Owner deleted successfully.'}, status=200)
		else:
			return JsonResponse({'error': 'No owner found with that id.'}, status=400)
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'}, status=405)
# Overview
# Takes a list of owners
# Returns an summarised view of the owners
# TODO: Check with Maclane to see if this is what he wants
def overview(data):
	overview = []
	for datum in data:
		overview.append({
			'id': datum['id'],
			'first_name': datum['first_name'],
			'last_name': datum['last_name'],
			'email': datum['email'],
		})
	return overview
# Find Pets
# Takes an owner
# Returns the owner with an embedded list of their pets
def find_pets(owner):
	pets = Animal.objects.filter(owner=owner['id'])
	owner['pets'] = []
	for pet in pets:
		owner['pets'].append({
			'id': pet.id,
			'name': pet.name,
			'species': pet.species,
		})
	return owner