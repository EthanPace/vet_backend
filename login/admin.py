from django.contrib import admin
from .models import User
from django.contrib.sessions.models import Session
from django.contrib.auth.models import Group, User as AuthUser
# register the User model from models.py
admin.site.register(User)
# register the Session model from django.contrib.sessions.models
admin.site.register(Session)
# unregister the Group and default user models from the admin site.
admin.site.unregister(Group)
admin.site.unregister(AuthUser)