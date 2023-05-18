from django.test import TestCase

# Create your tests here.

# SHOW ALL / GET ALL
# URL http://127.0.0.1:8000/animals/

# SHOW 1 / GET 1
# URL http://127.0.0.1:8000/animals/1/ - 1 at end is the ID for animal

# CREATE / POST
# URL http://127.0.0.1:8000/animals/create/
# Body
{
  "name": "Max",
  "age": 4,
  "breed": "Labrador Retriever",
  "species": "Dog",
  "colour": "Black",
  "weight": 25,
  "DOB": "2018-02-20",
  "vaccination_status": "Complete",
  "microchip_number": "789456123",
  "owner": 2
}
