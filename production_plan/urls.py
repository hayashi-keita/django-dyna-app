from django.urls import path
from .views.product_create import ProductCreateView
from .views.orderitem_process_create import OrderItemProcessCreateView
from .views.process_all_list import AllOrderItemProcessListView, ProcessListView
from .views.product_list import ProductListView
from .views.product_update import ProductUpdateView
from .views.product_schedule import OrderItemProcessCompleteView
from .views.orderitem_process_update import OrderItemProcessPlanView, OrderItemProcessStatusUpdateView, ProcessDateListView, ScheduleByProcessDateView
from django.shortcuts import render

app_name = 'production_plan'

urlpatterns = [
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('process/list/', ProcessListView.as_view(), name='process_list'),
    path('process/all/', AllOrderItemProcessListView.as_view(), name='orderitem_process_list_all'),
    path('process/<int:pk>/create/', OrderItemProcessCreateView.as_view(), name='orderitem_process_create'),
    path('process/<int:pk>/complete', OrderItemProcessCompleteView.as_view(), name='orderitem_process_complete'),
    path('orderitem_process/<int:pk>/plan/', OrderItemProcessPlanView.as_view(), name='orderitem_process_plan'),
    path('orderitem_process/<int:pk>/status/', OrderItemProcessStatusUpdateView.as_view(), name='status_update'),
    path('schedule/<int:pk>/dates/', ProcessDateListView.as_view(), name='process_date_list'),
    path('schedule/<int:pk>/process_date/<str:scheduled_date>/', ScheduleByProcessDateView.as_view(), name='schedule_by_process_date'),
    path('success/', lambda request: render(request, 'production_plan/success.html'), name='product_success'),
]