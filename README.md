# Supply Chain Management System

A web application built with **Django**, **PostgreSQL**, **Celery**, and **EDI file parsing** to manage inventory, customer orders, and shipments in a supply chain system. This system is deployed on an **Ubuntu VM** and can be served through **Nginx**.

## Features

- **Customer Management**: Store and manage customer information like name, email, phone, and address.
- **Inventory Management**: Manage products with SKU, name, description, quantity, and price.
- **Order Management**: Track orders placed by customers, including their status (pending, processing, shipped, cancelled).
- **Order Items**: Link each order with multiple items (inventory products) and manage their quantities.
- **Shipment Tracking**: Track the shipment status of orders with carriers like UPS, USPS, and FedEx.
- **EDI File Import**: Import customer orders and inventory data from EDI files and process them asynchronously.

## Tech Stack

- **Backend**: Django 4.x
- **Database**: PostgreSQL
- **Task Queue**: Celery
- **Message Broker**: Redis (configured as the broker for Celery)
- **Web Server**: Nginx (for production deployment)
- **File Parsing**: EDI (Electronic Data Interchange)

## Requirements

- **Ubuntu VM** (for the server setup)
- Python 3.8+
- PostgreSQL 12+
- Redis (for Celery)
- Celery
- Django 4.x
- Nginx (for deployment)

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/supply-chain-management.git
cd supply-chain-management
```

### 2. Create a virtual environment

``` bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
``` bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL on Ubuntu VM
- Install PostgreSQL and create a new database and user for the project.
``` bash
sudo -u postgres psql
CREATE DATABASE supplychain_db;
CREATE USER supplychain_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE supplychain_db TO supplychain_user;
```
- Update DATABASES in settings.py with your PostgreSQL credentials.

### 5. Apply database migrations
``` bash
python manage.py migrate
```

### 6. Create a superuser
``` bash
python manage.py createsuperuser
```

### 7. Run Celery (for asynchronous tasks)
- In a separate terminal window, start the Celery worker:
``` bash
celery -A supplychain worker --loglevel=info
```

### 8. Run the server
``` bash
python manage.py runserver
```
- Now you can access the admin interface at http://localhost:8000/admin.

## EDI File Processing
You can place **EDI files** (e.g., .edi or .txt) into the edi_files/incoming/ folder. The system will automatically import customer, inventory, and order data from these files when the following command is run:
``` bash
python manage.py import_edi
```
The EDI file should follow this format:

``` bash
CUSTOMER|John Doe|john.doe@example.com|+1234567890|123 Main St
INVENTORY|SKU123|Widget|A useful widget|10|15.99
ORDER|pending
ORDERITEM|SKU123|5
SHIPMENT|USPS|TRACK12345|shipped
```
Files will be moved to the edi_files/processed/ folder after they are successfully imported.

## Celery Task

Celery is set up to handle asynchronous tasks, such as processing orders. It uses Redis as the message broker to queue and process tasks.

## Usage

1. **Admin Panel**  
   You can manage customers, inventory, orders, and shipments via the Django admin panel at [http://localhost:8000/admin](http://localhost:8000/admin).

2. **EDI Import**  
   Import EDI files and create orders and inventory from external systems.

3. **Asynchronous Processing**  
   Celery ensures tasks like order processing are handled in the background, improving performance and user experience.


## Contributing

If you want to contribute to this project, please fork the repository and submit a pull request with your changes.

### Steps to contribute:

1. **Fork** the repository  
2. **Clone** your forked repository  
3. **Create** a new branch  
4. **Make** your changes  
5. **Test** your changes locally  
6. **Submit** a pull request to the main repository

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Notes

- **Nginx Configuration**:  
  Make sure to update the `your_domain_or_IP` and paths (`/path_to_your_project/static/`, `/path_to_your_project/media/`) with actual values that match your server setup.

- **Gunicorn**:  
  You'll want to run Gunicorn in the background or set it up to run as a service (for production) instead of manually starting it each time.
