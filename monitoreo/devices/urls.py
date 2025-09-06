from django.urls import path
from . import views

urlpatterns = [
    # Dispositivos
    path("devices/", views.device_list, name="device_list"),
    path("devices/create/", views.create_device, name="create_device"),
    path("devices/<int:device_id>/", views.device_detail, name="device_detail"),
    path("devices/<int:device_id>/edit/", views.edit_device, name="edit_device"),
    path("devices/<int:device_id>/delete/", views.delete_device, name="delete_device"),

    # Mediciones
    path("measurements/", views.measurement_list, name="measurement_list"),
]
