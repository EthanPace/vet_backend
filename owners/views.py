from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Owner
from .serializers import OwnerSerializer
from json import loads
from animals.models import Animal
# Index
# Takes no arguments
# Returns an overview of all owners
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
		return overview(serializer.data)
	else:
		return JsonResponse({'error': 'This endpoint only accepts GET requests.'})
# Details
# Takes an id as part of the endpoint
# Returns the full details of the owner with the given id
# TODO: figure out what this does
def details(request, id):
	if request.method == 'GET':
		owner = Owner.objects.filter(id=id)
		if owner:
			serializer = OwnerSerializer(owner[0])
			return JsonResponse(find_pets(serializer.data), safe=False)
		else:
			return JsonResponse({'error': 'No owner found with that id.'})
	else:
		return JsonResponse({'error': 'This endpoint only accepts GET requests.'})
# Add
# Create functionality for owners
# Takes all owner fields as part of the request body
# Returns the full details of the newly created owner
# TODO: Make sure this still works
@csrf_exempt
def add(request):
	if request.method == 'POST':
		body = request.body.decode('utf-8')
		data = loads(body)
		serial = OwnerSerializer(data=data)
		if serial.is_valid():
			serial.save()
			return JsonResponse(serial.data, safe=False)
		else:
			return JsonResponse({'error': 'Invalid data.'})
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'})
# Edit
# Update functionality for owners
# Takes an id as part of the endpoint and all owner fields as part of the request body
# Returns the id of the updated owner
@csrf_exempt
def edit(request, id):
	if request.method == 'POST':
		data = loads(request.body)
		owner = Owner.objects.filter(id=id)
		if owner:
			owner.update(first_name=data['first_name'], last_name=data['last_name'], phone_number=data['phone_number'], email=data['email'], availability=data['availability'], staff=data['staff'])
			return JsonResponse({'id': owner[0].id})
		else:
			return JsonResponse({'error': 'No owner found with that id.'})
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'})
# Delete
# Delete functionality for owners
# Takes an id as part of the endpoint
# Returns a success/fail message
# TODO: Test this
@csrf_exempt
def delete(request, id):
	if request.method == 'POST':
		owner = Owner.objects.filter(id=id)
		if owner:
			owner.delete()
			return JsonResponse({'success': 'Owner deleted successfully.'})
		else:
			return JsonResponse({'error': 'No owner found with that id.'})
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'})
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
	return JsonResponse(overview, safe=False)
# Find Pets
# Takes an owner
# Returns the owner with an embedded list of their pets
def find_pets(owner):
	pets = Animal.objects.filter(owner=owner['id'])
	owner['pets'] = pets
	return owner