from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer
from .models import User
from json import loads
from hashlib import sha256
@csrf_exempt
def login(request):
	if request.method == 'POST':
		# Get the request body
		body = loads(request.body)
		# Get the username and password from the request
		username = body.get('username')
		password = body.get('password')
		# Check if the username and password are correct
		user = authenticate(username=username, password=password)
		if user is not None:
			return JsonResponse({"result":"true"}, safe=False)
		else:
			return JsonResponse({"result":"false"}, safe=False)
	else:
		return JsonResponse({"result":"Wrong_Method_Error"}, safe=False)
@csrf_exempt
def register(request):
	if request.method == 'POST':
		# Get the request body
		body = loads(request.body)
		# Get the username and password from the request
		username = body.get('username')
		password = body.get('password')
		# Check if the username is already taken
		if User.objects.filter(username=username).exists():
			return JsonResponse({"result":"Username_Taken_Error"}, safe=False)
		else:
			# Create the user
			user = User(username=username, password=hash(password))
			user.save()
			return JsonResponse({"result":"success"}, safe=False)
	else:
		return JsonResponse({"result":"Wrong_Method_Error"}, safe=False)
	
def authenticate(username, password):
	# Check if the username and password are correct
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		user = None
	if user is not None:
		if user.password == hash(password):
			return user
		else:
			return None
	else:
		return None
	
def hash(string):
	# Hash the password
	return sha256(string.encode('utf-8')).hexdigest()