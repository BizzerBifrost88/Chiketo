from django.urls import path
from . import views

urlpatterns = [
    # Home Section
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.signup,name='signup'),
    path('venue/<int:venue_id>/', views.venue, name='venue'),
    path('event/', views.event, name='event'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart, name='cart'),

    # User
    path('home/',views.usermenu,name='usermenu'),
    path('home/user-setting/',views.usersetting,name='usersetting'),
    path('home/venue/<int:venue_id>/',views.uservenue,name='uservenue'),
    path('home/event/',views.userevent,name='userevent'),
    path('home/cart/',views.usercart,name='usercart'),
    path('home/contact/',views.usercontact,name='usercontact'),
    path('home/user-setting/update/',views.userupdate,name='userupdate'),
    path('home/user-setting/update/saveupdate/',views.saveupdate,name='saveupdate'),
    path('home/cart/pay/<int:booking_id>/', views.usercart_pay, name='usercart_pay'),
    path('home/cart/delete/<int:booking_id>/', views.usercart_delete, name='usercart_delete'),
    path('home/event/booking/<int:event_id>/', views.booking, name='booking'),
    path('home/event/booking/addcart/<int:event_id>/', views.addcart, name='addcart'),

    # Admin section
    path('admin-home/',views.adminmenu,name='adminmenu'),

    # Staff Section
    path('staff-home/',views.staffmenu,name='staffmenu'),
]