from django.contrib import admin
from .models import Category, Zone, Device, Measurement

admin.site.register([Category, Measurement, Zone])

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'consumption', 'status', 'category', 'zone')
    list_filter = ('status', 'category')
    search_fields = ('name',)
