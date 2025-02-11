# reservations/serializers.py
from rest_framework import serializers
from .models import Reservation, Customer, Restaurant, Table, Timeslot, Payment
from django.contrib.auth.hashers import make_password



class CustomerSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove the confirm_password field
        password = validated_data['password']
        validated_data['password'] = make_password(password)  # Hash the password before saving
        customer = Customer.objects.create(**validated_data)
        return customer


class RestaurantSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Restaurant
        fields = ['name', 'email', 'contact', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove the confirm_password field
        password = validated_data['password']
        validated_data['password'] = make_password(password)  # Hash the password before saving
        restaurant = Restaurant.objects.create(**validated_data)
        return restaurant

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'restaurant', 'tablenumber', 'seats']


class TimeslotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeslot
        fields = ['id', 'restaurant', 'starttime', 'endtime']


class ReservationSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    table = serializers.PrimaryKeyRelatedField(queryset=Table.objects.all())
    timeslot = serializers.PrimaryKeyRelatedField(queryset=Timeslot.objects.all())

    class Meta:
        model = Reservation
        fields = ['id', 'customer', 'table', 'timeslot', 'date', 'status']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'restaurant', 'amount', 'date']
