from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Room, Reservation, SpecialRate, RoomCategory
from .serializers import RoomSerializer, ReservationSerializer
from datetime import datetime, timedelta
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt

# Room Availability Check
@api_view(['GET'])
def check_availability(request):
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    category_id = request.query_params.get('category')

    available_rooms = Room.objects.filter(
        category__id=category_id, is_available=True
    ).exclude(
        Q(reservation__start_date__lte=end_date) & Q(reservation__end_date__gte=start_date)
    )
    # Check if any rooms are available
    if not available_rooms.exists():
        return Response({'message': 'No rooms available for the selected dates and category.'}, status=status.HTTP_404_NOT_FOUND)
    # return available rooms
    serializer = RoomSerializer(available_rooms, many=True)
    return Response(serializer.data)

# Create Reservation
@csrf_exempt  
@api_view(['POST'])
def create_reservation(request):
    data = request.data
    room = Room.objects.get(id=data['room'])
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    
    # Check for overlapping reservations
    if Reservation.objects.filter(
        room=room, start_date__lte=end_date, end_date__gte=start_date
    ).exists():
        return Response({'error': 'Room is already reserved for this period.'}, status=status.HTTP_400_BAD_REQUEST)

    # Calculate number of nights
    number_of_nights = (end_date - start_date).days
    if number_of_nights <= 0:
        return Response({'error': 'End date must be after start date.'}, status=status.HTTP_400_BAD_REQUEST)

    # Initialize total price
    total_price = Decimal(0.0)
    category = room.category
    base_price = category.base_price  # Base price of the room per night

    # Iterate over each day of the reservation
    current_date = start_date
    while current_date < end_date:
        # Check if there's a special rate for the current date
        special_rate = SpecialRate.objects.filter(
            room_category=category, start_date__lte=current_date, end_date__gte=current_date
        ).first()
        
        # Apply special rate if it exists, otherwise use base price
        rate_multiplier = special_rate.rate_multiplier if special_rate else Decimal(1.0)
        daily_price = base_price * rate_multiplier
        total_price += daily_price
        
        # Move to the next day
        current_date += timedelta(days=1)

    # Create the reservation
    reservation = Reservation.objects.create(
        room=room,
        start_date=start_date,
        end_date=end_date,
        customer_name=data['customer_name'],
        total_price=total_price
    )
    
    serializer = ReservationSerializer(reservation)
    return Response(serializer.data, status=status.HTTP_201_CREATED)