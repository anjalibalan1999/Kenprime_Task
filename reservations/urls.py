from django.urls import path
from . import views

urlpatterns = [
    path('availability/', views.check_availability, name='check_availability'),
    path('reservation/', views.create_reservation, name='create_reservation'),
]
