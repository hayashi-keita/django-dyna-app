from django.contrib import admin
from .models import Location, Customer, Product, Order, OrderItem, UserProfile, DeliveryDestinaion

admin.site.register(Location)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(UserProfile)
admin.site.register(DeliveryDestinaion)

