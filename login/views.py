from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from json import loads
from hashlib import sha256
# Login
# Takes a username and password as part of the request body
# Returns the id and role of the user with the given username and password
@csrf_exempt
def login(request):
	if request.method == 'POST':
		if request.session.get('logged_in', False) == False:
			data = loads(request.body)
			user = User.objects.filter(username=data['username'], password=hash(data['password']))
			if user:
				request.session['logged_in'] = True
				request.session['user_id'] = user[0].id
				request.session['user_role'] = user[0].role
				return JsonResponse({'result':'success'}, status=200)
			else:
				return JsonResponse({'error': 'No user found with that username and password.'}, status=400)
		else:
			return JsonResponse({'error': 'A user is already logged in.'}, status=409)
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'}, status=405)
# Logout
# Takes no arguments
# Returns a success message if the user was logged out successfully
@csrf_exempt
def logout(request):
	if request.session['logged_in']:
		request.session.flush()
		return JsonResponse({'result': 'success'}, status=200)
	else:
		return JsonResponse({'error': 'No user logged in.'}, status=409)
# Register
# Add functionality for users
# Takes a username and password as part of the request body
# Returns the id and role of the newly created user
@csrf_exempt
def register(request):
	if request.method == 'POST':
		data = loads(request.body)
		user = User.objects.filter(username=data['username'])
		if user:
			return JsonResponse({'error': 'A user with that username already exists.'}, status=409)
		else:
			user = User.objects.create(username=data['username'], password=hash(data['password']), role=data['role'])
			return JsonResponse({"result":"success", "data":{'id': user.id,'name':user.username, 'role': user.role}}, status=201)
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'}, status=405)
# Edit
# Update functionality for users
# Takes an id as part of the endpoint and all user fields as part of the request body
# Returns the id and role of the updated user
@csrf_exempt
def edit(request, id):
	if request.method == 'POST':
		data = loads(request.body)
		user = User.objects.filter(id=id)
		if user:
			user.update(username=data['username'], password=hash(data['password']), role=data['role'])
			return JsonResponse({"result":"success","data":{'id': user[0].id, 'role': user[0].role, "hashcheckREMOVE":user[0].password}}, safe=False, status=200)
		else:
			return JsonResponse({'error': 'No user found with that id.'}, status=400)
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'}, status=405)
# Delete
# Delete functionality for users
# Takes an id as part of the endpoint
# Returns a success message if the user was deleted successfully
@csrf_exempt
def delete(request, id):
	if request.method == 'POST':
		user = User.objects.filter(id=id)
		if user:
			user.delete()
			return JsonResponse({'result': 'success'}, status=200)
		else:
			return JsonResponse({'error': 'No user found with that id.'}, status=400)
	else:
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'}, status=405)
# Hash
# Hash functionality for passwords
# Takes a password as part of the request body
# Returns the hashed password
def hash(password):
	return sha256(password.encode('utf-8')).hexdigest()
