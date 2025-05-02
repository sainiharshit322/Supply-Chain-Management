from django.urls import path
from . import views

urlpatterns = [
    path('inventory-report/', views.inventory_report_view, name='inventory_report'),
    path('inventory-report/pdf/<int:month>/<int:year>/', views.inventory_report_pdf, name='inventory_report_pdf'),
]

