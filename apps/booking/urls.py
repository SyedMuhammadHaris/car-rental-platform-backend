from django.urls import path
from apps.booking.views.booking_view import BookingView

urlpatterns = [
    path("booking", BookingView.as_view(), name="booking"),
]