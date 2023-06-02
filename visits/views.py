from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import Visit
from .serializers import VisitSerializer
from json import loads
from animals.models import Animal
# Index
# Takes no arguments
# Returns an overview of all visits
def index(request):
	# check if the request method is GET
	if request.method == 'GET':
		# check if the page and page_size parameters are in the request
		if 'page' in request.GET:
			# get the page and page_size parameters from the request
			page = int(request.GET.get('page', 1))
			page_size = int(request.GET.get('page_size', 10))
			# get the visits for the given page
			visits = Visit.objects.all()[(page - 1) * page_size:page * page_size]
		else:
			# get all visits
			visits = Visit.objects.all()
		# serialize the visits
		serializer = VisitSerializer(visits, many=True)
		# return the overview of the full list of visits
		return JsonResponse(overview(serializer.data), safe=False, status=200)
	else:
		# return an error if the request method is not GET
		return JsonResponse({'error': 'This endpoint only accepts GET requests.'}, status=405)
# Details
# Takes an id as part of the endpoint
# Returns the full details of the visit with the given id
def details(request, id):
	# check if the request method is GET
	if request.method == 'GET':
		# find the visit with the given id
		visit = Visit.objects.filter(id=id)
		# check if the visit exists
		if visit:
			# serialize the visit (not entirely sure why this is necessary)
			serializer = VisitSerializer(visit[0])
			serializer.data['animal'] = find_animal(serializer.data['animal']).name
			# return the serialized visit data
			return JsonResponse(serializer.data, safe=False, status=200)
		else:
			# return an error if the visit doesn't exist
			return JsonResponse({'error': 'No visit found with that id.'}, status=400)
	else:
		# return an error if the request method is not GET
		return JsonResponse({'error': 'This endpoint only accepts GET requests.'}, status=405)
# Add
# Create functionality for visits
# Takes all visit fields as part of the request body
# Returns the full details of the newly created visit
@csrf_exempt
def add(request):
	# check if the request method is POST
	if request.method == 'POST':
		# get the request body and load as json
		body = request.body.decode('utf-8')
		data = loads(body)
		# check if the animal exists
		if find_animal(data['animal']):
			# convert the date_time string to a datetime object
			data['date_time'] =	date(data['date_time'])
			# serialize the visit
			serial = VisitSerializer(data=data)
			# check if the visit is valid
			if serial.is_valid():
				# save the visit
				serial.save()
				# return the serialized visit data
				return JsonResponse({"result":"success", "id":serial.data["id"]}, safe=False, status=201)
			else:
				# return an error if the visit is not valid
				return JsonResponse({'error': 'Invalid data.', 'messages': serial.error_messages}, status=400)
		else:
			# return an error if the animal doesn't exist
			return JsonResponse({'error': 'No animal found with that id.'}, status=400)
	else:
		# return an error if the request method is not POST
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'}, status=405)
# Edit
# Update functionality for visits
# Takes an id as part of the endpoint and all visit fields as part of the request body
# Returns the id of the updated visit
@csrf_exempt
def edit(request, id):
	# check if the request method is PUT
	if request.method == 'PUT':
		# get the request body and load as json
		data = loads(request.body)
		# check if the visit exists
		visit = Visit.objects.filter(id=id)
		# check if the visit exists
		if visit:
			# serialize the visit
			serial = VisitSerializer(data=data)
			# check if the visit is valid
			if serial.is_valid():
				visit.update(**serial.validated_data)
			else:
				# return an error if the visit is not valid
				return JsonResponse({'error': 'Invalid data.', 'messages':serial.error_messages}, status=400)
			# return the id of the updated visit
			return JsonResponse({"result":"success", 'id': visit[0].id}, safe=False, status=200)
		else:
			# return an error if the visit doesn't exist
			return JsonResponse({'error': 'No visit found with that id.'}, status=400)
	else:
		# return an error if the request method is not PUT
		return JsonResponse({'error': 'This endpoint only accepts PUT requests.'}, status=405)
# Delete
# Delete functionality for visits
# Takes an id as part of the endpoint
# Returns a success message if the visit was deleted successfully
@csrf_exempt
def delete(request, id):
	# check if the request method is DELETE
	if request.method == 'DELETE':
		# find the visit with the given id
		visit = Visit.objects.filter(id=id)
		# check if the visit exists
		if visit:
			# delete the visit
			visit.delete()
			# return a success message
			return JsonResponse({'success': 'Visit deleted successfully.'}, status=200)
		else:
			# return an error if the visit doesn't exist
			return JsonResponse({'error': 'No visit found with that id.'}, status=400)
	else:
		# return an error if the request method is not DELETE
		return JsonResponse({'error': 'This endpoint only accepts DELETE requests.'}, status=405)
# Overview
# Takes a list of owners
# Returns an summarised view of the owners
# TODO: Check with Maclane if this is what he needs here
def overview(data):
	# create an empty list to store the overview
	overview = []
	# loop through the visits
	for datum in data:
		# append the id and date_time to the overview
		overview.append({
			'id': datum['id'],
			'date_time': datum['date_time'],
			'animal':find_animal(datum['animal']).name
		})
	# return the overview
	return overview
# Find Animal
# Takes a visit
# Returns the animal associated with the visit
def find_animal(data):
	# get the animal with the given id
	animal = Animal.objects.filter(id=data)
	# check if the animal exists
	if animal:
		data = animal[0]
	# return the animal
	return data
# Date
# Takes a date_time string
# Returns a datetime object
def date(date_time):
	return datetime.strptime(date_time, '%Y-%m-%d %H:%M')