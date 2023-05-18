from django.test import TestCase

# Create your tests here.

# SHOW ALL / GET ALL
# URL http://127.0.0.1:8000/owners

# SHOW 1 / GET 1
# URL http://127.0.0.1:8000/owners/1 - 1 = ID for owner

# CREATE / POST
# URL http://127.0.0.1:8000/owners/create/
# Body:
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "johndoe@example.com",
  "phone_number": "1234567890",
  "available_times": "9am-5pm"
}
