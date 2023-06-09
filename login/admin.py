from django.contrib import admin
from .models import User, AuthToken
from django.contrib.auth.models import Group, User as AuthUser
# register the User model from models.py
admin.site.register(User)
# register the AuthToken model from models.py
admin.site.register(AuthToken)
# unregister the Group and default user models from the admin site.
admin.site.unregister(Group)
admin.site.unregister(AuthUser)