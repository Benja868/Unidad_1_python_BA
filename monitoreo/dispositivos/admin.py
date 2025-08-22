from django.contrib import admin
from .models import Dispositivo

@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "consumo_maximo", "categoria", "zona")
    search_fields = ("nombre", "categoria", "zona")
