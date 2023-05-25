from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Visit
from .serializers import VisitSerializer
from json import loads
from animals.models import Animal
# Index
# Takes no arguments
# Returns an overview of all visits
# TODO: Add Authorization
# TODO: Test this
def index(request):
	if request.method == 'GET':
		if 'page' in request.GET:
			page = int(request.GET['page', 1])
			page_size = int(request.GET['page_size', 10])
			visits = Visit.objects.all()[(page - 1) * page_size:page * page_size]
		else:
			visits = Visit.objects.all()
		serializer = VisitSerializer(visits, many=True)
		return JsonResponse(overview(serializer.data), safe=False, status=200)
	else:
		return JsonResponse({'error': 'This endpoint only accepts GET requests.'}, status=405)
# Details
# Takes an id as part of the endpoint
# Returns the full details of the visit with the given id
# TODO: Add Authorization
# TODO: Test this
def details(request, id):
	if request.method == 'GET':
		visit = Visit.objects.filter(id=id)
		if visit:
			serializer = VisitSerializer(visit[0])
			return JsonResponse(find_animal(serializer.data), safe=False, status=200)
		else:
			return JsonResponse({'error': 'No visit found with that id.'}, status=400)
	else:
		return JsonResponse({'error': 'This endpoint only accepts GET requests.'}, status=405)
# Add
# Create functionality for visits
# Takes all visit fields as part of the request body
# Returns the full details of the newly created visit
# TODO: Add Authorization
# TODO: Test this
@csrf_exempt
def add(request):
	if request.method == 'POST':
		body = request.body.decode('utf-8')
		data = loads(body)
		if find_animal(data['animal']):
			serial = VisitSerializer(data=data)
			if serial.is_valid():
				serial.save()
				return JsonResponse({"result":"success", "data":serial.data}, safe=False, status=201)
			else:
				return JsonResponse({'error': 'Invalid data.'}, status=400)
		else:
			return JsonResponse({'error': 'No animal found with that id.'}, status=400)
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'}, status=405)
# Edit
# Update functionality for visits
# Takes an id as part of the endpoint and all visit fields as part of the request body
# Returns the id of the updated visit
# TODO: Fix the fields on the update line
# TODO: Add Authorization
# TODO: Test this
@csrf_exempt
def edit(request, id):
	if request.method == 'PUT':
		data = loads(request.body)
		visit = Visit.objects.filter(id=id)
		if visit:
			visit.update()
			return JsonResponse({"result":"success", 'id': visit[0].id}, safe=False, status=200)
		else:
			return JsonResponse({'error': 'No visit found with that id.'}, status=400)
	else:
		return JsonResponse({'error': 'This endpoint only accepts PUT requests.'}, status=405)
# Delete
# Delete functionality for visits
# Takes an id as part of the endpoint
# Returns a success message if the visit was deleted successfully
# TODO: Add Authorization
# TODO: Test this
@csrf_exempt
def delete(request, id):
	if request.method == 'DELETE':
		visit = Visit.objects.filter(id=id)
		if visit:
			visit.delete()
			return JsonResponse({'success': 'Visit deleted successfully.'}, status=200)
		else:
			return JsonResponse({'error': 'No visit found with that id.'}, status=400)
	else:
		return JsonResponse({'error': 'This endpoint only accepts DELETE requests.'}, status=405)
# Overview
# Takes a list of owners
# Returns an summarised view of the owners
# TODO: Check with Maclane if this is what he needs here
def overview(data):
	overview = []
	for datum in data:
		overview.append({
			'id': datum['id'],
			'date_time': datum['date_time'],
		})
	return overview
# Find Animal
# Takes a visit
# Returns the animal associated with the visit
def find_animal(data):
	animal = Animal.objects.filter(id=data['animal'])
	if animal:
		data['animal'] = animal[0]
	return data