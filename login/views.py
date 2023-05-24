from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .serializers import UserSerializer
from json import loads
from hashlib import sha256
# Login
# Takes a username and password as part of the request body
# Returns the id and role of the user with the given username and password
# TODO: Add Authorization
@csrf_exempt
def login(request):
	if request.method == 'POST':
		data = loads(request.body)
		user = User.objects.filter(username=data['username'], password=hash(data['password']))
		if user:
			request.session['logged_in'] = True
			request.session['user_id'] = user[0].id
			request.session['user_role'] = user[0].role
			return JsonResponse({'result':'true'})
		else:
			return JsonResponse({'error': 'No user found with that username and password.'})
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'})
# Logout
# Takes no arguments
# Returns a success message if the user was logged out successfully
def logout(request):
	if request.session['logged_in']:
		request.session.flush()
		return JsonResponse({'success': 'User logged out successfully.'})
	else:
		return JsonResponse({'error': 'No user logged in.'})
# Register
# Add functionality for users
# Takes a username and password as part of the request body
# Returns the id and role of the newly created user
# TODO: Test this
@csrf_exempt
def register(request):
	if request.method == 'POST':
		data = loads(request.body)
		user = User.objects.filter(username=data['username'])
		if user:
			return JsonResponse({'error': 'A user with that username already exists.'})
		else:
			user = User.objects.create(username=data['username'], password=hash(data['password']))
			return JsonResponse({'id': user.id, 'role': user.role})
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'})
# Edit
# Update functionality for users
# Takes an id as part of the endpoint and all user fields as part of the request body
# Returns the id and role of the updated user
# TODO: Test this
@csrf_exempt
def edit(request, id):
	if request.method == 'POST':
		data = loads(request.body)
		user = User.objects.filter(id=id)
		if user:
			user.update(username=data['username'], password=hash(data['password']))
			return JsonResponse({'id': user[0].id, 'role': user[0].role})
		else:
			return JsonResponse({'error': 'No user found with that id.'})
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'})
# Delete
# Delete functionality for users
# Takes an id as part of the endpoint
# Returns a success message if the user was deleted successfully
# TODO: Test this
@csrf_exempt
def delete(request, id):
	if request.method == 'POST':
		user = User.objects.filter(id=id)
		if user:
			user.delete()
			return JsonResponse({'success': 'User deleted successfully.'})
		else:
			return JsonResponse({'error': 'No user found with that id.'})
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'})
# Hash
# Hash functionality for passwords
# Takes a password as part of the request body
# Returns the hashed password
# TODO: Test this
def hash(password):
	return sha256(password.encode('utf-8')).hexdigest()
