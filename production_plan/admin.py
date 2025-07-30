from django.contrib import admin
from .models import Process, ProductProcess, OrderItemProcess

admin.site.register(Process)
admin.site.register(ProductProcess)
admin.site.register(OrderItemProcess)
