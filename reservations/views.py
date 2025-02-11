from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from .models import Customer, Restaurant, Reservation, Table, Timeslot
from .serializers import CustomerSerializer, RestaurantSerializer, ReservationSerializer, TableSerializer, TimeslotSerializer

# JWT Token Generation
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Customer Sign-Up
class CustomerSignupView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# Restaurant Sign-Up
class RestaurantSignupView(generics.CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

# Login View for Customer and Restaurant
class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        # Check for customer
        customer = Customer.objects.filter(email=email).first()
        if customer and check_password(password, customer.password):
            tokens = get_tokens_for_user(customer)
            return Response({"role": "customer", "tokens": tokens}, status=status.HTTP_200_OK)

        # Check for restaurant
        restaurant = Restaurant.objects.filter(email=email).first()
        if restaurant and check_password(password, restaurant.password):
            tokens = get_tokens_for_user(restaurant)
            return Response({"role": "restaurant", "tokens": tokens}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# Create Reservation (Customer only)
class ReservationCreateView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Associate the logged-in customer with the reservation
        serializer.save(customer=self.request.user)

# CRUD for Restaurant (Only Restaurant)
class RestaurantDashboardView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return reservations for the logged-in restaurant
        return Reservation.objects.filter(table__restaurant=self.request.user)

    def perform_create(self, serializer):
        # Create reservation for the restaurant
        restaurant = self.request.user
        serializer.save(restaurant=restaurant)

# List of all Customers (Only Restaurant/Authorized Users)
class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()  # Get all customers
    serializer_class = CustomerSerializer

# List of all Restaurants (Only Restaurant/Authorized Users)
class RestaurantListView(generics.ListAPIView):
    queryset = Restaurant.objects.all()  # Get all restaurants
    serializer_class = RestaurantSerializer

# List of all Tables (Filter by restaurant_id)
class TableListView(generics.ListAPIView):
    serializer_class = TableSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return Table.objects.filter(restaurant__id=restaurant_id)

# List of all Reservations
class ReservationListView(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

# List of all Time Slots
class TimeSlotListView(generics.ListAPIView):
    queryset = Timeslot.objects.all()
    serializer_class = TimeslotSerializer
