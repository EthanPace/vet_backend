from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import User, AuthToken
from json import loads
from hashlib import sha256
from random import randint
# Details
# Takes an id as part of the endpoint
# Returns the full details of the user with the given id (except password)
def details(request, id):
	# check if the request method is GET
	if request.method == 'GET':
		# check for an authtoken in the request headers and whether the token exists
		token = AuthToken.objects.filter(token=request.headers.get('authtoken', ''))
		# check if the token exists
		if not token:
			# return an error if the token doesn't exist
			return JsonResponse({'error': 'You must be logged in to view this page.'}, status=401)
		# check if the user is logged in as an admin or the user with the given id
		if token.user_role == 'admin' or token.user_id == id:
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
			# return an error if the user is not logged in as an admin or the user with the given id
			return JsonResponse({'error': 'You must be logged in as an admin or the user with the given id to view this page.'}, status=401)
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
		# get the request body and load as json
		data = loads(request.body)
		# try to find a user with the given username and password
		user = User.objects.filter(username=data['username'], password=hash(data['password']))
		# check if the user exists
		if user:
			# log the user in by creating a new authtoken
			token = AuthToken.objects.create(token=generate_token(), user_id=user[0].id, user_role=user[0].role).token
			# return the id and role of the user
			return JsonResponse({'result':'success', "id":user[0].id, "token":token}, status=200)
		else:
			# return an error if the user doesn't exist
			return JsonResponse({'error': 'No user found with that username and password.'}, status=400)
	else:
		# return an error if the request method is not POST
		return JsonResponse({'error': 'This endpoint only accepts POST requests.'}, status=405)
# Logout
# Takes no arguments
# Returns a success message if the user was logged out successfully
@csrf_exempt
def logout(request):
	# check if the header contains an authtoken
	if 'authtoken' in request.headers:
		# find the authtoken
		token = AuthToken.objects.filter(token=request.headers['authtoken'])
		# check if the authtoken exists
		if token:
			# delete the authtoken
			token.delete()
			# return a success message
			return JsonResponse({'result': 'success'}, status=200)
		else:
			# return an error if the authtoken doesn't exist
			return JsonResponse({'error': 'No user logged in with that authtoken.'}, status=400)
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
		# check for an authtoken in the request headers
		token = AuthToken.objects.filter(token=request.headers.get('authtoken', ''))
		# check if the authtoken exists
		if not token:
			# return an error if the authtoken doesn't exist
			return JsonResponse({'error': 'You must be logged in to edit a user.'}, status=401)
		# check if the user is logged in as an admin or the user with the given id
		if token[0].user_role == 'admin' or token[0].user_id == id:
			# get the request body and load as json
			data = loads(request.body)
			user = User.objects.filter(id=id)
			# check if the user exists
			if user:
				# update the user
				user[0].update(username=data['username'], password=hash(data['password']), role=data['role'])
				# return the id and role of the updated user
				return JsonResponse({"result":"success","data":{'id': user[0].id, 'role': user[0].role}}, safe=False, status=200)
			else:
				# return an error if the user doesn't exist
				return JsonResponse({'error': 'No user found with that id.'}, status=400)
		else:
			# return an error if the user is not logged in as an admin or the user with the given id
			return JsonResponse({'error': 'You must be logged in as an admin or the user with the given id to view this page.'}, status=401)
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
		# check for an authtoken in the request headers
		token = AuthToken.objects.filter(token=request.headers.get('authtoken', ''))
		# check if the authtoken exists
		if not token:
			# return an error if the authtoken doesn't exist
			return JsonResponse({'error': 'You must be logged in to delete a user.'}, status=401)
		# check if the user is logged in as an admin or the user with the given id
		if token[0].user_role == 'admin' or token[0].user_id == id:
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
			# return an error if the user is not logged in as an admin or the user with the given id
			return JsonResponse({'error': 'You must be logged in as an admin or the user with the given id to view this page.'}, status=401)
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
# Generate Token
# Generate a token for a user
def generate_token():
	# generate a token
	return sha256((str(randint(99,1000000)) + str(datetime.now)).encode('utf-8')).hexdigest()
