from django.urls import path
from . import landing, views, client
urlpatterns = [
    # region LANDING PAGE ==========================================================================================
    path('', client.userhome, name='userhome'),
    path('login_user', landing.login_user, name='login_user'),
    path('signup/', landing.signup, name='signup'),
    path('home', landing.home, name='home'),
    path('logout/',landing.logout_user, name='logout'),
    
    path('check_seat_status/<coach_id>/', client.check_seat_status, name='check_seat_status'),

    # region ADMIN =================================================================================================
    path('adminhome/', views.adminhome, name='adminhome'),
    path('journey_create/', views.journey_create, name='journey_create'),

    # region CLIENT ==============================================================================================
    path('coach_select/', client.coach_select, name='coach_select'),
    path('seat_select/', client.seat_select, name='seat_select'),
    path('booking_summary/', client.booking_summary, name='booking_summary'),
    path('booking_view/', client.booking_view, name='booking_view'),
    path('booking_select/', client.booking_select, name='booking_select'),

    # WEBSITE SETTING
    path('app_setting/',landing.app_setting, name='app_setting'),
    
]