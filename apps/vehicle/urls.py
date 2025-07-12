from django.contrib import admin
from django.urls import path

from apps.vehicle.views.vehicle_detail_view import VehicleDetailView
from apps.vehicle.views.vehicle_view import VehicleView


urlpatterns = [
    path("vehicle", VehicleView.as_view(), name="vehicle"),
    path("vehicle/<int:vehicle_id>", VehicleDetailView.as_view(), name="vehicle_detail"),
]
