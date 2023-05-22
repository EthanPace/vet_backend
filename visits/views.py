from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Visit
from .serializers import VisitSerializer
from json import loads
# Index
# Takes no arguments
# Returns an overview of all visits
# TODO: Add pagination
# TODO: Add Authorization
# TODO: Test this
def index(request):
	if request.method == 'GET':
		visits = Visit.objects.all()
		serializer = VisitSerializer(visits, many=True)
		return overview(serializer.data)
	else:
		return JsonResponse({'error': 'This endpoint only accepts GET requests.'})
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
			return JsonResponse(serializer.data, safe=False)
		else:
			return JsonResponse({'error': 'No visit found with that id.'})
	else:
		return JsonResponse({'error': 'This endpoint only accepts GET requests.'})
# Search
# Takes a search term and search text as part of the request body
# Returns a list of visits matching the search term and search text
# TODO: Implement, add auth, run tests
def search(request):
	return JsonResponse({'error': 'This endpoint is not implemented yet.'})
	if request.method == 'POST':
		data = loads(request.body)
		visits = Visit.objects.filter(name__icontains=data['name'])
		serializer = VisitSerializer(visits, many=True)
		return JsonResponse(serializer.data, safe=False)
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'})
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
		serial = VisitSerializer(data=data)
		if serial.is_valid():
			serial.save()
			return JsonResponse(serial.data, safe=False)
		else:
			return JsonResponse({'error': 'Invalid data.'})
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'})
# Edit
# Update functionality for visits
# Takes an id as part of the endpoint and all visit fields as part of the request body
# Returns the id of the updated visit
# TODO: Fix the fields on the update line
# TODO: Add Authorization
# TODO: Test this
@csrf_exempt
def edit(request, id):
	if request.method == 'POST':
		data = loads(request.body)
		visit = Visit.objects.filter(id=id)
		if visit:
			visit.update(name=data['name'], age=data['age'], species=data['species'], breed=data['breed'], color=data['color'], weight=data['weight'], height=data['height'], description=data['description'])
			return JsonResponse({'id': visit[0].id})
		else:
			return JsonResponse({'error': 'No visit found with that id.'})
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'})
# Delete
# Delete functionality for visits
# Takes an id as part of the endpoint
# Returns a success message if the visit was deleted successfully
# TODO: Add Authorization
# TODO: Test this
@csrf_exempt
def delete(request, id):
	if request.method == 'POST':
		visit = Visit.objects.filter(id=id)
		if visit:
			visit.delete()
			return JsonResponse({'success': 'Visit deleted successfully.'})
		else:
			return JsonResponse({'error': 'No visit found with that id.'})
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'})
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
			'animal_name': datum['animal']['name'],
			'animal_species': datum['animal']['species'],
		})
	return JsonResponse(overview, safe=False)