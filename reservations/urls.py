# reservations/urls.py
from django.urls import path
from .views import CustomerSignupView, RestaurantSignupView, LoginView, ReservationCreateView, RestaurantDashboardView, CustomerListView, ReservationListView, TableListView, RestaurantListView, TimeSlotListView

urlpatterns = [
    path('signup/customer/', CustomerSignupView.as_view(), name='customer-signup'),
    path('signup/restaurant/', RestaurantSignupView.as_view(), name='restaurant-signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('reservations/create/', ReservationCreateView.as_view(), name='reservation-create'),
    path('restaurant/dashboard/', RestaurantDashboardView.as_view(), name='restaurant-dashboard'),
    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurants/<int:restaurant_id>/tables/', TableListView.as_view(), name='table-list'),
    path('reservations/', ReservationListView.as_view(), name='reservation-list'),
    path('timeslots/', TimeSlotListView.as_view(), name='timeslot-list'),
]
