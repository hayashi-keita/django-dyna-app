from django.db import models
from orders.models import OrderItem

# 車両
class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=20, unique=True, verbose_name='車両番号')
    driver_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='ドライバー名')
    capacity = models.PositiveIntegerField(null=True, blank=True, verbose_name='積載量（㎡）')
    is_active = models.BooleanField(default=True, verbose_name='稼働中')

    def __str__(self):
        return f'{self.vehicle_number} ({self.driver_name or "無名"})'

# 配車予定
class DeliverySchedule(models.Model):
    STATUS_CHOICES = [
        ('unassigned', '未配車'),
        ('assigning', '配車中'),
        ('planned', '配車確定'),
        ('dispatched', '出荷済'),
        ('completed', '納品完了'),
    ]

    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, verbose_name='対象注文明細')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='車両')
    delivery_date = models.DateField(null=True, blank=True, verbose_name='配送日')
    departure_time = models.TimeField(null=True, blank=True, verbose_name=' 出発時間')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='usassigned', verbose_name='ステータス')
    note = models.CharField(max_length=200, null=True, blank=True, verbose_name='備考')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='配送順')

    class Meta:
        ordering = ['delivery_date', 'departure_time']
    
    def __str__(self):
        return f'{self.order_item} - {self.get_status_display()}'