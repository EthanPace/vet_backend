from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Note
from .serializers import NoteSerializer
from json import loads, dumps

# def show(request, id):
#     note = Note.objects.get(id=id)
#     return JsonResponse(note.to_dict(), safe=False)

def show(request, id):
    note = Note.objects.get(id=id)
    serializer = NoteSerializer(note)
    return JsonResponse(serializer.data, safe=False)

# def show_all(request):
#     notes = Note.objects.all()
#     serialized_notes = [note.to_dict() for note in notes]
#     return JsonResponse(serialized_notes, safe=False)

def show_all(request):
    notes = Note.objects.all()
    serializer = NoteSerializer(notes, many=True)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def create(request):
	note = loads(request.body)
	serializer = NoteSerializer(data=note)
	if serializer.is_valid():
		serializer.save()
		return JsonResponse(serializer.data, safe=False)
	return JsonResponse(serializer.errors, safe=False)
@csrf_exempt
def update(request, id):
	note = Note.objects.get(id=id)
	updated_note = loads(request.body)
	serializer = NoteSerializer(note, data=updated_note)
	if serializer.is_valid():
		serializer.save()
		return JsonResponse(serializer.data, safe=False)
	return JsonResponse(serializer.errors, safe=False)
@csrf_exempt
def delete(request, id):
	note = Note.objects.get(id=id)
	note.delete()
	return JsonResponse("Deleted note with id: " + str(id), safe=False)
