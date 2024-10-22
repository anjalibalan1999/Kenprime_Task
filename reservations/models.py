from django.db import models

class RoomCategory(models.Model):
    name = models.CharField(max_length=50)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Room(models.Model):
    room_number = models.CharField(max_length=10)
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.room_number

class SpecialRate(models.Model):
    room_category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    rate_multiplier = models.DecimalField(max_digits=4, decimal_places=2, default=1.0)

class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    customer_name = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['room', 'start_date', 'end_date'], name='unique_reservation'
            )
        ]

    def __str__(self):
        return f'Reservation for {self.customer_name}'
