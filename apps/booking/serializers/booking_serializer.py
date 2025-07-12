from rest_framework.serializers import ModelSerializer

from apps.booking.models.booking import Booking
from rest_framework import serializers
from django.utils import timezone
from apps.vehicle.models import Vehicle
from constants.common_status import CommonStatus
from utils.common import get_date

class BookingSerializer(ModelSerializer):
    # start_date = serializers.DateTimeField()
    # end_date = serializers.DateTimeField()
    
    class Meta:
        model = Booking
        fields =["user", "vehicle", "start_date", "end_date"]
 
    def create(self, validated_data):
        booking = Booking(
            user=validated_data["user"],
            vehicle=validated_data["vehicle"],
            start_date=validated_data["start_date"],
            end_date=validated_data["end_date"],
            status=CommonStatus.ACTIVE.value,
        )
        booking.save()
        return booking
    
    def to_representation(self, instance):
        return {
            "object": "booking",
            "id": instance.id,
            "user_id": instance.user_id,
            "vehicle_id": instance.vehicle_id,
            "start_date": get_date(instance.start_date),
            "end_date": get_date(instance.end_date),
            "status": instance.status,
            "created_at": get_date(instance.created_at),
            "updated_at": get_date(instance.updated_at),
        }

