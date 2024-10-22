from django.contrib import admin
from .models import RoomCategory, Room, Reservation, SpecialRate

@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_price']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'category', 'is_available']

@admin.register(SpecialRate)
class SpecialRateAdmin(admin.ModelAdmin):
    list_display = ['room_category', 'start_date', 'end_date', 'rate_multiplier']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['room', 'start_date', 'end_date', 'customer_name', 'total_price']
