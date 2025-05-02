import os
from django.core.management.base import BaseCommand
from inventory.models import Customer, Inventory, Order, OrderItem, Shipment
from django.utils.timezone import now

EDI_PATH = "edi_files/incoming/"
PROCESSED_PATH = "edi_files/processed/"

class Command(BaseCommand):
    help = "Imports EDI files and creates orders"

    def handle(self, *args, **kwargs):
        # Loop through the EDI files in the incoming directory
        for filename in os.listdir(EDI_PATH):
            filepath = os.path.join(EDI_PATH, filename)
            if filename.endswith(".edi") or filename.endswith(".txt"):
                with open(filepath, 'r') as file:
                    lines = file.read().strip().split('\n')

                    customer = None
                    order = None

                    # Parse each line in the EDI file
                    for line in lines:
                        parts = line.split('|')
                        
                        # Handle customer data
                        if parts[0] == "CUSTOMER":
                            name, email, phone, address = parts[1:]
                            customer, created = Customer.objects.get_or_create(
                                email=email,
                                defaults={"name": name, "phone": phone, "address": address}
                            )
                            if created:
                                self.stdout.write(self.style.SUCCESS(f"Created customer: {name}"))
                            else:
                                self.stdout.write(self.style.SUCCESS(f"Found existing customer: {name}"))
                        
                        # Handle inventory data
                        elif parts[0] == "INVENTORY":
                            sku, name, desc, qty, price = parts[1:]
                            inventory, created = Inventory.objects.get_or_create(
                                sku=sku,
                                defaults={
                                    "name": name,
                                    "description": desc,
                                    "quantity": int(qty),
                                    "price": float(price)
                                }
                            )
                            if created:
                                self.stdout.write(self.style.SUCCESS(f"Created inventory item: {name}"))
                            else:
                                self.stdout.write(self.style.SUCCESS(f"Found existing inventory item: {name}"))
                        
                        # Handle order data
                        elif parts[0] == "ORDER":
                            status = parts[1]
                            order = Order.objects.create(customer=customer, status=status)
                            self.stdout.write(self.style.SUCCESS(f"Created order for {customer.name} with status {status}"))
                        
                        # Handle order item data
                        elif parts[0] == "ORDERITEM":
                            sku, qty = parts[1:]
                            item = Inventory.objects.get(sku=sku)
                            OrderItem.objects.create(order=order, inventory=item, quantity=int(qty))
                            self.stdout.write(self.style.SUCCESS(f"Added item {item.name} to order {order.id}"))
                        
                        # Handle shipment data
                        elif parts[0] == "SHIPMENT":
                            carrier, tracking, status = parts[1:]
                            Shipment.objects.create(
                                order=order, 
                                carrier=carrier, 
                                tracking_number=tracking, 
                                status=status
                            )
                            self.stdout.write(self.style.SUCCESS(f"Created shipment for order {order.id}"))

                    # Move the file to the processed folder
                    os.rename(filepath, os.path.join(PROCESSED_PATH, filename))
                    self.stdout.write(self.style.SUCCESS(f"Processed and moved file: {filename}"))

