from django.contrib import admin
from .models import Customer, Inventory, Order, OrderItem, Shipment

admin.site.register(Customer)
admin.site.register(Inventory)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Shipment)

