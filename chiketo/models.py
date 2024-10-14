from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class User(models.Model):
    userID=models.AutoField(primary_key=True)
    name=models.TextField()
    email=models.EmailField(unique=True)
    phone=models.TextField()
    password=models.TextField()
    def __str__(self):
        return f"{self.name}"

class Staff(models.Model):
    staffID=models.AutoField(primary_key=True)
    name=models.TextField()
    email=models.EmailField(unique=True)
    phone=models.TextField()
    password=models.TextField()
    def __str__(self):
        return f"{self.name}"
      
class Admin(models.Model):
    adminID=models.AutoField(primary_key=True)
    name=models.TextField()
    email=models.EmailField(unique=True)
    phone=models.TextField()
    password=models.TextField()
    def __str__(self):
        return f"{self.name}"
    
class Venue(models.Model):
    venueID=models.AutoField(primary_key=True)
    name=models.TextField()
    def __str__(self):
        return f"{self.name}"

class Event(models.Model):  
    eventID=models.AutoField(primary_key=True)
    name=models.TextField()
    start=models.DateTimeField()
    end=models.DateTimeField()
    price=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    venueID=models.ForeignKey(Venue, on_delete=models.CASCADE)
    staffID=models.ForeignKey(Staff, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name}"

class Booking(models.Model):
    PAYMENT = [
        ('not pay', 'Not Pay'),
        ('paid', 'Paid'),   
    ]
    bookingID=models.AutoField(primary_key=True)
    userID=models.ForeignKey(User, on_delete=models.CASCADE)
    eventID=models.ForeignKey(Event, on_delete=models.CASCADE)
    pay=models.TextField(choices=PAYMENT,default='not pay')
    