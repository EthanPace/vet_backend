from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Owner
from .serializers import OwnerSerializer
from json import loads, dumps


# def show(request, id):
#     owner = Owner.objects.get(id=id)
#     return JsonResponse(owner.to_dict(), safe=False)

def show(request, id=None):
    if id:
        # Retrieve a single owner by ID
        owner = Owner.objects.get(id=id)
        return JsonResponse(owner.to_dict(), safe=False)
    else:
        # Retrieve all owners
        owners = Owner.objects.all()
        owners_list = [owner.to_dict() for owner in owners]
        return JsonResponse(owners_list, safe=False)

def show_all_owners(request):
    owners = Owner.objects.all()
    owners_list = [owner.to_dict() for owner in owners]
    return JsonResponse(owners_list, safe=False)

@csrf_exempt
def create(request):
    owner = loads(request.body)
    serializer = OwnerSerializer(data=owner)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse(serializer.errors, safe=False)


@csrf_exempt
def update(request, id):
    owner = Owner.objects.get(id=id)
    updated_owner = loads(request.body)
    serializer = OwnerSerializer(owner, data=updated_owner)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse(serializer.errors, safe=False)


@csrf_exempt
def delete(request, id):
    owner = Owner.objects.get(id=id)
    owner.delete()
    return JsonResponse("Deleted owner with id: " + str(id), safe=False)
