from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.name

class Inventory(models.Model):
    sku = models.CharField(max_length=100, unique=True)  # Stock Keeping Unit
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.sku})"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('cancelled', 'Cancelled')
    ], default='pending')

    def __str__(self):
        return f"Order #{self.id} for {self.customer.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.inventory.name}"

class Shipment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    shipped_date = models.DateTimeField(null=True, blank=True)
    tracking_number = models.CharField(max_length=255, blank=True)
    carrier = models.CharField(max_length=50, choices=[
        ('UPS', 'UPS'),
        ('USPS', 'USPS'),
        ('FedEx', 'FedEx')
    ])
    status = models.CharField(max_length=50, default='in_transit')

    def __str__(self):
        return f"Shipment for Order #{self.order.id}"

