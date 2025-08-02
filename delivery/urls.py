from django.urls import path
from .views.delivery_list import AssignVehicleView, UnassignedListView, DailyDispatchView
from .views.status_update import StatusUpdateView
from .views.vehicle_create import VehicleCreateView, VehicleListView, VehicleUpdateView, VehicleDeleteView
from .views.assigning import AssigningListView, AssigningVehicleListView, BulkConfirView

app_name = 'delivery'

urlpatterns = [
    path('unassigned/', UnassignedListView.as_view(), name='unassigned_list'),
    path('assigning/', AssigningListView.as_view(), name='assigning_list'),
    path('assign/<int:pk>/', AssignVehicleView.as_view(), name='assign_vehicle'),
    
    path('status_update/<int:pk>/<str:status>/', StatusUpdateView.as_view(), name='status_update'),
    path('daily/', DailyDispatchView.as_view(), name='daily_dispatch'),
    path('vehicles/', VehicleListView.as_view(), name='vehicle_list'),
    path('vehicles/create/', VehicleCreateView.as_view(), name='vehicle_create'),
    path('vehicle/<int:pk>/update/', VehicleUpdateView.as_view(), name='vehicle_update'),
    path('vehicle/<int:pk>/delete/', VehicleDeleteView.as_view(), name='vehicle_delete'),
]