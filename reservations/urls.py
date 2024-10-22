from django.urls import path
from . import views

urlpatterns = [
    path('availability/', views.check_availability, name='check_availability'), #eg: http://127.0.0.1:8000/api/availability/?start_date=2000-11-08&end_date=2000-11-10&category=1
    path('reservation/', views.create_reservation, name='create_reservation'),  #eg: http://127.0.0.1:8000/api/reservation/

]
