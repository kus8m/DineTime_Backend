from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    tablenumber = models.PositiveIntegerField()
    seats = models.PositiveIntegerField()
    
    def __str__(self):
        return f"Table {self.tablenumber} - {self.restaurant.name}"

class Customer(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    
    def __str__(self):
        return self.username

class Timeslot(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    starttime = models.TimeField()
    endtime = models.TimeField()
    
    def __str__(self):
        return f"{self.starttime} - {self.endtime} ({self.restaurant.name})"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(Timeslot, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"Reservation {self.id} - {self.customer.username} on {self.date}"

class Payment(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    
    def __str__(self):
        return f"Payment {self.id} - {self.restaurant.name} - {self.amount}"
