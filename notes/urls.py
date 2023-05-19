from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_all, name='show_all_notes'),
    path('<int:id>/', views.show),
    path('create/', views.create),
    path('update/<int:id>/', views.update),
    path('delete/<int:id>/', views.delete),
]