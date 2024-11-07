from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomeView.as_view(), name='home'),
    path('add-customer/', views.AddCustomerView.as_view(), name='add_customer'),
    path('create-invoice/', views.CreateInvoiceView.as_view(), name='create_invoice'),
]