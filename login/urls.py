from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
	path('register/', views.register, name='register'),
	path('edit/<int:id>', views.edit, name='edit'),
	path('delete/<int:id>', views.delete, name='delete'),
]