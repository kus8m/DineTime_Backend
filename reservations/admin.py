from django.contrib import admin
from .models import Restaurant, Table, Customer, Timeslot, Reservation, Payment

admin.site.register(Restaurant)
admin.site.register(Table)
admin.site.register(Customer)
admin.site.register(Timeslot)
admin.site.register(Reservation)
admin.site.register(Payment)