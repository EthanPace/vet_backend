from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from json import loads
from hashlib import sha256
# Details
# Takes an id as part of the endpoint
# Returns the full details of the user with the given id (except password)
def details(request, id):
	# check if the request method is GET
	if request.method == 'GET':
		# find the user with the given id
		user = User.objects.filter(id=id)
		# check if the user exists
		if user:
			# return the serialized user data
			return JsonResponse({'id': user[0].id, 'username': user[0].username, 'role': user[0].role}, status=200)
		else:
			# return an error if the user doesn't exist
			return JsonResponse({'error': 'No user found with that id.'}, status=400)
	else:
		# return an error if the request method is not GET
		return JsonResponse({'error': 'This endpoint only accepts GET requests.'}, status=405)
# Login
# Takes a username and password as part of the request body
# Returns the id and role of the user with the given username and password
@csrf_exempt
def login(request):
	# check if the request method is POST
	if request.method == 'POST':
		# check if the user is already logged in
		if request.session.get('logged_in', False) == False:
			# get the request body and load as json
			data = loads(request.body)
			# try to find a user with the given username and password
			user = User.objects.filter(username=data['username'], password=hash(data['password']))
			# check if the user exists
			if user:
				# log the user in
				request.session['logged_in'] = True
				request.session['user_id'] = user[0].id
				request.session['user_role'] = user[0].role
				# return the id and role of the user
				return JsonResponse({'result':'success', "id":user[0].id}, status=200)
			else:
				# return an error if the user doesn't exist
				return JsonResponse({'error': 'No user found with that username and password.'}, status=400)
		else:
			# return an error if a user is already logged in
			return JsonResponse({'error': 'A user is already logged in.'}, status=409)
	else:
		# return an error if the request method is not POST
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'}, status=405)
# Logout
# Takes no arguments
# Returns a success message if the user was logged out successfully
@csrf_exempt
def logout(request):
	# check if the user is logged in
	if request.session.get('logged_in', False) == True:
		# log the user out
		request.session.flush()
		# return a success message
		return JsonResponse({'result': 'success'}, status=200)
	else:
		# return an error if a user is not logged in
		return JsonResponse({'error': 'No user logged in.'}, status=409)
# Register
# Add functionality for users
# Takes a username and password as part of the request body
# Returns the id and role of the newly created user
@csrf_exempt
def register(request):
	# check if the request method is POST
	if request.method == 'POST':
		# get the request body and load as json
		data = loads(request.body)
		role = data.get('role', 'user')
		# try to find a user with the given username
		user = User.objects.filter(username=data['username'])
		# check if the user exists
		if user:
			# return an error if the user already exists
			return JsonResponse({'error': 'A user with that username already exists.'}, status=409)
		else:
			# create a new user with the given data
			user = User.objects.create(username=data['username'], password=hash(data['password']), role=role)
			# return a success message with the new user data
			return JsonResponse({"result":"success", 'id': user.id}, status=201)
	else:
		# return an error if the request method is not POST
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'}, status=405)
# Edit
# Update functionality for users
# Takes an id as part of the endpoint and all user fields as part of the request body
# Returns the id and role of the updated user
@csrf_exempt
def edit(request, id):
	# check if the request method is PUT
	if request.method == 'PUT':
		# get the request body and load as json
		data = loads(request.body)
		user = User.objects.filter(id=id)
		# check if the user exists
		if user[0].username == data['username'] and user[0].password == hash(data['old_password']):
			# update the user
			user.update(username=data['username'], password=hash(data['password']), role=data['role'])
			# return the id and role of the updated user
			return JsonResponse({"result":"success","data":{'id': user[0].id, 'role': user[0].role}}, safe=False, status=200)
		else:
			# return an error if the user doesn't exist
			return JsonResponse({'error': 'Incorrect credentials.'}, status=400)
	else:
		# return an error if the request method is not PUT
		return JsonResponse({'error': 'This endpoint only accepts PUT requests.'}, status=405)
# Delete
# Delete functionality for users
# Takes an id as part of the endpoint
# Returns a success message if the user was deleted successfully
@csrf_exempt
def delete(request, id):
	# check if the request method is DELETE
	if request.method == 'DELETE':
		# find the user with the given id
		user = User.objects.filter(id=id)
		# check if the user exists
		if user:
			# get the id of the user to be deleted
			id = user[0].id
			# delete the user
			user.delete()
			# return a success message
			return JsonResponse({'result': 'success', 'id':id}, status=200)
		else:
			# return an error if the user doesn't exist
			return JsonResponse({'error': 'No user found with that id.'}, status=400)
	else:
		# return an error if the request method is not DELETE
		return JsonResponse({'error': 'This endpoint only accepts DELETE requests.'}, status=405)
# Hash
# Hash functionality for passwords
# Takes a password as part of the request body
# Returns the hashed password
def hash(password):
	# hash the password
	return sha256(password.encode('utf-8')).hexdigest()
