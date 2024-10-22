from rest_framework import serializers
from .models import RoomCategory, Room, SpecialRate, Reservation

class RoomCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomCategory
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class SpecialRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialRate
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
