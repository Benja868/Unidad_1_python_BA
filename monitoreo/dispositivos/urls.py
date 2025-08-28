from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),  # Página principal
    path("panel/", views.panel, name="panel"),
    path('admin/', admin.site.urls),
    path('inicio/', views.inicio, name="inicio"),  # Vista inicio
    path('dispositivos/', views.inicio, name="dispositivos"),  # Vista de dispositivos
    path('dispositivos/<int:dispositivo_id>/', views.dispositivo, name="dispositivo"),  # Detalle del dispositivo
]