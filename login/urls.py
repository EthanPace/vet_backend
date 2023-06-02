from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
	path('logout/', views.logout, name='logout'),
	path('register/', views.register, name='register'),
    path('users/details/<int:id>', views.details, name='details'),
	path('users/edit/<int:id>', views.edit, name='edit'),
	path('users/delete/<int:id>', views.delete, name='delete'),
]