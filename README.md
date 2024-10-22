# change the mysql database password and username 

# make sure to migrate the models using this commands
  python manage.py makemigrations
  python manage.py migrate
  python manage.py runserver

# Add room data through shell
python manage.py shell
from reservations.models import Room, RoomCategory

# create room category
RoomCategory.objects.create(name=''Deluxe", base_price=100.00)
RoomCategory.objects.create(name='Standard')', base_price=50.00)

mysql> select * from reservations_roomcategory; # mysql data look like this
+----+----------+------------+
| id | name     | base_price |
+----+----------+------------+
|  1 | Deluxe   |     100.00 |
|  2 | Standard |      50.00 |
+----+----------+------------+
2 rows in set (0.00 sec)


# Fetch the room categories
deluxe_category = RoomCategory.objects.get(name='Deluxe')
standard_category = RoomCategory.objects.get(name='Standard')

# Add multiple room data at once
Room.objects.bulk_create([
    Room(room_number='101', category=deluxe_category, is_available=True),
    Room(room_number='102', category=deluxe_category, is_available=True),
    Room(room_number='103', category=standard_category, is_available=True),
    Room(room_number='104', category=standard_category, is_available=True),
    Room(room_number='105', category=standard_category, is_available=True),
])
Room.objects.all()

mysql> select * from reservations_room; # mysql data look like this
+----+-------------+--------------+-------------+
| id | room_number | is_available | category_id |
+----+-------------+--------------+-------------+
|  1 | 101         |            1 |           1 |
|  2 | 102         |            1 |           1 |
|  3 | 103         |            1 |           2 |
|  4 | 104         |            1 |           2 |
|  5 | 105         |            1 |           2 |
+----+-------------+--------------+-------------+


# add special rates model
from your_app.models import SpecialRate, RoomCategory
from datetime import date
from decimal import Decimal

# give a already created room category 
category = RoomCategory.objects.get(id=1)

# Add a special rate for the category between specific dates
special_rate = SpecialRate.objects.create(
    room_category=category,
    start_date=date(2024, 12, 1),
    end_date=date(2024, 12, 31),
    rate_multiplier=Decimal('1.5')  # 50% price increase for this period
)
special_rate.save()

mysql> select * from reservations_specialrate;  # mysql data look like this
+----+------------+------------+-----------------+------------------+
| id | start_date | end_date   | rate_multiplier | room_category_id |
+----+------------+------------+-----------------+------------------+
|  1 | 2024-12-01 | 2024-12-31 |            1.50 |                1 |
|  2 | 2020-11-08 | 2000-10-10 |            1.50 |                1 |
+----+------------+------------+-----------------+------------------+


# Here Iam using postman to test this code
1) create a request to add reservation
    method=post
    path:  http://127.0.0.1:8000/api/reservation/

   in body session give data like this example:
     {
    "room": 6,
    "start_date": "2024-12-1",
    "end_date": "2024-12-31",
    "customer_name": "anjali"
     }

2) create a request to find available rooms
    method=get
    path:  http://127.0.0.1:8000/api/availability/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&category=category_id
    example: http://127.0.0.1:8000/api/availability/?start_date=2000-11-08&end_date=2000-11-10&category=1
    


