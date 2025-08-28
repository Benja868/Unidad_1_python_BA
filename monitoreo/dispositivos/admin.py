from django.contrib import admin
from .models import Categoria, Zona, Dispositivo, Medicion

admin.site.register([Categoria, Medicion, Zona])

@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
    list_display = ('nombre','consumo','estado','categoria','zona')
    list_filter = ('estado', 'categoria')
    search_fields = ('nombre',)