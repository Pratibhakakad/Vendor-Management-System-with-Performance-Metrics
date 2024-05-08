# Vendor Management System with Performance Metrics

The Vendor Management System is a Django application designed to track and analyze vendor performance metrics, manage purchase orders, and provide comprehensive insights into vendor performance over time.

## clone the repository:git clone https://github.com/Pratibhakakad Vendor-Management-System-with-Performance-Metrics.git
## cd vendor
## Install dependencies: pip install -r requirements.txt
## run migration:python manage.py migrate
## create superuser:python manage.py createsuperuser
## start the development server:python manage.py runserver
## API Endpoints:
## Vendor details:'GET/api/vendors/<uuid:pk>/'
## purchaseorder detail:'GET/api/purchase_order/<uuid:pk>'
## Vendor Performance Endpoint:'GET/api/vendors/{vendor_code}/performance'
## Update Acknowledgment Endpoint: POST /api/purchase_orders/{po_number}/acknowledge'
## Token authentication: follow test.rest file
## Documentation of API endpoints:http://127.0.0.1:8000/swagger/
