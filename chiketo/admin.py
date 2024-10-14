from django.contrib import admin
from .models import User, Staff, Admin, Venue, Event, Booking

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    pass

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    pass

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    pass

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass