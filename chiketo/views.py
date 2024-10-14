from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from chiketo.models import User, Staff, Admin, Venue, Booking, Event
from datetime import datetime
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
# Create your views here.

#Home Section
def index(request):
    myevent = Event.objects.count()
    myuser = User.objects.count()
    bookings = Booking.objects.filter(pay='paid').count()
    venues = Venue.objects.all().values()
    
    context = {
        'myevent': myevent,
        'myuser': myuser,
        'bookings':bookings,
        'venues': venues,
    }
    return render(request, 'home/index.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email') #ni ambik dari yang input name contoh:<input type='text' name='EMAIL'> jangan ikut bold just nak tunjuk je
        password = request.POST.get('password')

        user = search(User, email)
        staff = search(Staff, email)
        admin = search(Admin, email)

        if user:
            if user.password == password:
                request.session['user_type'] = 'user' # ni declare user type je tukar ikut user type website 
                request.session['user_id'] = user.userID  
                return redirect('usermenu')
            else:
                messages.error(request, "Password is incorrect.")
        elif staff:
            if staff.password == password:
                request.session['user_type'] = 'staff'
                request.session['user_id'] = staff.staffID
                return redirect('staffmenu')
            else:
                messages.error(request, "Password is incorrect.")
        elif admin:
            if admin.password == password:
                request.session['user_type'] = 'admin'
                request.session['user_id'] = admin.adminID
                return redirect('adminmenu')
            else:
                messages.error(request, "Password is incorrect.")
        else:
            messages.error(request, "Email not found. Please sign up first.")

    venues = Venue.objects.all().values()
    context = {
        'venues':venues,
    }

    return render(request, 'home/login.html', context)

def search(model, email):
    try:
        return model.objects.get(email=email)
    except model.DoesNotExist:
        return None

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if password == confirm_password:
            if User.objects.filter(email=email).exists() or Staff.objects.filter(email=email).exists() or Admin.objects.filter(email=email).exists():
                messages.error(request, 'The email has been taken. Please try again.')
            else:
                try:
                    user = User(name=name, email=email, phone=phone, password=password)
                    user.save()
                    messages.success(request, 'Sign up successful! You can now log in.')
                    return redirect('login')
                except Exception as e:
                    messages.error(request, 'Error occurred while signing up. Please try again.')
        else:
            messages.error(request, 'Passwords do not match. Please try again.')
    
    venues = Venue.objects.all().values()
    context = {
        'venues':venues,
    }


    return render(request, 'home/signup.html', context)


def logout(request):
    request.session.flush()
    messages.info(request, "You have been logged out.")
    return redirect('login')

def venue(request, venue_id):
    myvenue = Venue.objects.get(venueID=venue_id)
    venues = Venue.objects.all()
    events=Event.objects.filter(venueID=venue_id)
    
    context = {
        'myvenue' : myvenue,
        'venues': venues,
        'events':events,
    }
    return render(request, 'home/venue.html', context)

def event(request):
    events = Event.objects.all()
    venues = Venue.objects.all().values()

    
    context = {
        'events': events,
        'venues':venues,
    }
    return render(request, 'home/event.html', context)

def contact(request):
    address = "KOLEJ PROFESSIONAL MARA INDERA MAHKOTA, JALAN SUNGAI LEMBING, 25200 KUANTAN, PAHANG."
    email = "asmawiaiman@gmail.com"
    phone_number = "+6017-620 7253"
    developer_name = "Asmawi Aiman"

    venues = Venue.objects.all()
    context = {
        'address': address,
        'email': email,
        'phone_number': phone_number,
        'developer_name': developer_name,
        'venues':venues,
    }
    return render(request, 'home/contact.html', context)

def cart(request):
    
    events = Event.objects.all()
    venues = Venue.objects.all()

    context={
        'events':events,
        'venues':venues,
    }
    return render(request,'home/cart.html',context)

#User section
def usermenu(request):
    user_id = request.session.get('user_id')
    if not request.session.get('user_type') == 'user':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again")
        return redirect('login')  
    
    myevent = Event.objects.count()
    myuser = User.objects.count()
    mybooking = Booking.objects.filter(userID=user_id,pay='not pay').count()
    bookings = Booking.objects.filter(pay='paid').count()
    venues = Venue.objects.all().values()
    
    context = {
        'myevent': myevent,
        'myuser': myuser,
        'mybooking': mybooking,
        'venues': venues,
        'bookings':bookings,
        'user_id':user_id,
    }
    return render(request, 'user/usermenu.html', context)

def booking(request, event_id):
    user_id = request.session.get('user_id')
    if not request.session.get('user_type') == 'user':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again")
        return redirect('login')  
    
    mybooking = Booking.objects.filter(userID=user_id, pay='not pay').count()
    user = User.objects.get(userID=user_id)
    events = Event.objects.get(eventID=event_id)
    name = user.name
    venues = Venue.objects.all().values()
    context = {
        'name': name,
        'venues': venues,
        'events': events,
        'mybooking': mybooking,
    }
    return render(request, 'user/booking.html', context)

def usersetting(request):
    user_id = request.session.get('user_id')
    if not request.session.get('user_type') == 'user':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again")
        return redirect('login')
    mybooking = Booking.objects.filter(userID=user_id,pay='not pay').count()
    users=User.objects.get(userID=user_id)
    name=users.name
    email=users.email
    phone=users.phone
    password=users.password
    venues=Venue.objects.all()
    context = {
        'mybooking': mybooking,
        'name': name,
        'email': email,
        'phone': phone,
        'password': password,
        'user_id':user_id,
        'venues':venues,
    }
    
    return render(request,'user/usersetting.html',context)

def userevent(request):
    user_id = request.session.get('user_id')
    if not request.session.get('user_type') == 'user':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again")
        return redirect('login')
    events = Event.objects.all()
    venues=Venue.objects.all()
    mybooking = Booking.objects.filter(userID=user_id,pay='not pay').count()
    context = {
        'events': events,
        'venues':venues,
        'mybooking':mybooking,
    }
    return render(request, 'user/userevent.html', context)

def uservenue(request, venue_id):
    user_id = request.session.get('user_id')
    if not request.session.get('user_type') == 'user':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again")
        return redirect('login')
    myvenue = Venue.objects.get(venueID=venue_id)
    venues = Venue.objects.all().values()
    events=Event.objects.filter(venueID=venue_id)
    mybooking = Booking.objects.filter(userID=user_id,pay='not pay').count()
    
    context = {
        'myvenue' : myvenue,
        'venues': venues,
        'events':events,
        'mybooking': mybooking,
    }
    return render(request, 'user/uservenue.html', context)

def usercart(request):
    user_id = request.session.get('user_id')
    if not request.session.get('user_type') == 'user':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again")
        return redirect('login')
    
    venues = Venue.objects.all()
    mybooking = Booking.objects.filter(userID=user_id,pay='not pay').count()
    bookings=Booking.objects.filter(userID=user_id)
    
    context = {
        'venues': venues,
        'mybooking': mybooking,
        'bookings': bookings,
    }
    return render(request, 'user/usercart.html', context)

def usercart_pay(request, booking_id):
    if request.method == 'POST':
        booking = Booking.objects.get(bookingID=booking_id)
        booking.pay = 'paid'
        booking.save()
        messages.success(request, "Payment successful")
    return redirect('usercart')

def usercart_delete(request, booking_id):
    if request.method == 'POST':
        booking = Booking.objects.get(bookingID=booking_id)
        booking.delete()
        messages.success(request, "Booking deleted successfully")
    return redirect('usercart')

def usercontact(request):
    user_id = request.session.get('user_id')
    if not request.session.get('user_type') == 'user':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again")
        return redirect('login')
    
    venues = Venue.objects.all()
    address = "KOLEJ PROFESSIONAL MARA INDERA MAHKOTA, JALAN SUNGAI LEMBING, 25200 KUANTAN, PAHANG."
    email = "asmawiaiman@gmail.com"
    phone_number = "+6017-620 7253"
    developer_name = "Asmawi Aiman"

    mybooking = Booking.objects.filter(userID=user_id,pay='not pay').count()
  
    
    context = {
        'venues': venues,
        'mybooking': mybooking,
        'address':address,
        'email':email,
        'phone_number':phone_number,
        'developer_name':developer_name,
    }
    return render(request, 'user/usercontact.html', context)

def userupdate(request):
    user_id = request.session.get('user_id')
    if not request.session.get('user_type') == 'user':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again")
        return redirect('login')
    
    venues = Venue.objects.all().values()
    mybooking = Booking.objects.filter(userID=user_id,pay='not pay').count()
    user = User.objects.get(userID=user_id)
    name = user.name
    phone = user.phone
    email = user.email

  
    
    context = {
        'venues': venues,
        'mybooking': mybooking,
        'name':name,
        'phone':phone,
        'email':email,
    }

    return render(request, 'user/userupdate.html', context)


def saveupdate(request):
    user_id = request.session.get('user_id')
    if not request.session.get('user_type') == 'user':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again")
        return redirect('login')
    
    user = User.objects.get(userID=user_id)
    c_name = request.POST['name']
    c_phone = request.POST['phone']
    c_email = request.POST['email']
    c_password = request.POST['password']
    confirm = request.POST['confirm']
    password=user.password
    
    if c_password == password:
        if confirm == c_password:
            try:
                user.name = c_name
                user.phone=c_phone
                user.email=c_email
                user.save()
                messages.success(request, 'Update successfully!')
                return HttpResponseRedirect(reverse('usersetting'))
            except Exception as e: 
                messages.error(request, 'Error occured while changing detail. Please try again.')
                return HttpResponseRedirect(reverse('userupdate'))
        else:
            messages.error(request,'Passwords do not match. Please try again.')
            return HttpResponseRedirect(reverse('userupdate'))
    else:
        messages.error(request,'Wrong password. Please try again.')
        return HttpResponseRedirect(reverse('userupdate'))
    

def addcart(request, event_id):
    user_id = request.session.get('user_id')
    if not request.session.get('user_type') == 'user':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again")
        return redirect('login')
    
    if not Booking.objects.filter(userID=user_id, eventID=event_id, pay='not pay').exists():
        data = Booking(userID_id=user_id, eventID_id=event_id)
        data.save()
        messages.success(request, 'Added to cart successfully!')
    else:
        messages.info(request, 'This event is already in your cart.')
    
    return HttpResponseRedirect(reverse('usermenu'))



#Admin Section
def adminmenu(request):
    user_id = request.session.get('user_id')
    if not request.session.get('user_type') == 'admin':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again")
        return redirect('login')
    if request.method == "POST":
        if request.POST.get('email'):
            email = request.POST.get('email')
            if User.objects.filter(email=email).exists() or Staff.objects.filter(email=email).exists() or Admin.objects.filter(email=email).exists():
                messages.error(request, 'The email has been taken. Please try again.')
            else:
                try:
                    password = request.POST.get('password')
                    name = request.POST.get('name')
                    phone = request.POST.get('phone')
                    data = Staff(name=name,phone=phone,email=email,password=password)
                    data.save()
                    messages.success(request, 'Staff Added')
                except Exception as e:
                    messages.error(request, 'Error occurred while registering. Please try again.')
        elif request.POST.get('staff_id'):
            staff_id = request.POST.get('staff_id')
            if Staff.objects.filter(staffID=staff_id).exists():
                try:
                    Staff.objects.filter(staffID=staff_id).delete()
                    messages.success(request, 'Staff Deleted')
                except Exception as e:
                    messages.error(request, 'Error occurred while deleting. Please try again.')
            else:
                messages.error(request, 'This ID does not exist. Please use a different ID.') 
        elif request.POST.get('staffid'):
            staffID = request.POST.get('staffid')
            if Staff.objects.filter(staffID=staffID).exists():
                s_name = request.POST.get('sname')
                s_phone = request.POST.get('sphone')
                s_email = request.POST.get('semail')
                s_password = request.POST.get('spassword')
                s_confirm = request.POST.get('confirm')
                staff = Staff.objects.get(staffID=user_id)
                password = staff.password

                if s_password == password:
                    if s_confirm == s_password:
                        try:
                            Staff.objects.filter(staffID=staffID).update(name=s_name,phone=s_phone,email=s_email)
                            messages.success(request, 'Update successfully!')
                        except Exception as e:
                            messages.error(request, 'Error occurred while updating. Please try again.')
            
            else:
                messages.error(request, 'This ID does not exist. Please use a different ID.') 
        elif request.POST.get('venue_name'):
            try:
                name = request.POST.get('venue_name')
                data = Venue(name=name)
                data.save()
                messages.success(request, 'Venue Added')
            except Exception as e:
                messages.error(request, 'Error occurred while registering. Please try again.')

        elif request.POST.get('venue_id'):
            venue_id = request.POST.get('venue_id')
            if Venue.objects.filter(venueID=venue_id).exists():
                try:
                    Venue.objects.filter(venueID=venue_id).delete()
                    messages.success(request, 'Venue Deleted')
                except Exception as e:
                    messages.error(request, 'Error occurred while deleting. Please try again.')
            else:
                messages.error(request, 'This ID does not exist. Please use a different ID.')
    
    admin = Admin.objects.get(adminID=user_id)
    name = admin.name
    staffs = Staff.objects.all()
    nstaffs = Staff.objects.all().count()
    venues=Venue.objects.all()
    nvenues=Venue.objects.all().count()
    context = {
        'staffs': staffs,
        'nstaffs': nstaffs,
        'name': name,
        'venues':venues,
        "nvenues":nvenues,
    }
    return render(request, 'admin/adminmenu.html', context)

# Staff Section
def staffmenu(request):
    user_id = request.session.get('user_id')
    if not request.session.get('user_type') == 'staff':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again")
        return redirect('login')
    
    user = Staff.objects.get(staffID=user_id)
    name = user.name
    venues = Venue.objects.all()
    nvenues = Venue.objects.all().count()
    events = Event.objects.filter(staffID=user_id)
    sevents = Event.objects.filter(staffID=user_id).count()
    
    if request.method == "POST":
        if request.POST.get('name'):
            name = request.POST.get('name')
            price = request.POST.get('price')
            start = request.POST.get('start')
            end = request.POST.get('end')
            venue_id = request.POST.get('venue_id')
            try:
                venue = Venue.objects.get(venueID=venue_id)
                event = Event(name=name, price=price, start=start, end=end, venueID=venue, staffID=user)
                event.save()
                messages.success(request, 'Event Added')
            except Venue.DoesNotExist:
                messages.error(request, 'Venue does not exist. Please try again.')
        elif request.POST.get('event_id'):
            event_id = request.POST.get('event_id')
            try:
                event = Event.objects.get(eventID=event_id, staffID=user_id)
                event.delete()
                messages.success(request, 'Event Deleted')
            except Event.DoesNotExist:
                messages.error(request, 'Event does not exist or you do not have permission to delete it.')
    
    context = {
        'name': name,
        'venues': venues,
        'nvenues': nvenues,
        'events': events,
        'sevents': sevents,
    }
    return render(request, 'staff/staffmenu.html', context)
