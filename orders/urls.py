from django.urls import path
from django.shortcuts import render
from orders.views.order_create import OrderCreateView
from orders.views.order_list import OrderListView
from orders.views.order_detail import OrderDetailView
from orders.views.order_edit import OrderUpdateView

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('list/', OrderListView.as_view(), name='order_list'),
    path('detail/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('edit/<int:pk>/', OrderUpdateView.as_view(), name='order_edit'),
    path('success/', lambda request: render(request, 'orders/success.html'), name='order_success'),
]