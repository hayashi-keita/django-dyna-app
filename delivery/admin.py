from django.contrib import admin
from .models import Vehicle, DeliverySchedule

# 車両管理画面
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_number', 'driver_name', 'capacity', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('vehicle_number', 'driver_name')

# 配送予定管理画面
@admin.register(DeliverySchedule)
class DeliveryScheduleAdmin(admin.ModelAdmin):
    list_display = ('order_item', 'vehicle', 'delivery_date', 'departure_time', 'status')
    list_filter = ('status', 'delivery_date', 'vehicle')
    search_fields = (
        'order_item__product__name',
        'order_item__order__order_number',
        'vehicle__vehicle_number',
    )
    ordering = ['delivery_date', 'departure_time']