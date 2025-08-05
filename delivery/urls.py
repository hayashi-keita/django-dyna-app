from django.urls import path
from .views.status_update import StatusUpdateView
from .views.vehicle_create import VehicleCreateView, VehicleListView, VehicleUpdateView, VehicleDeleteView
from .views.assigning import UpdateSortOrderView, AssigningDateListView
from .views.unassigned import UnassignedListView, BulkAssignView
from .views.vehicle_base import (
    AssigningVehicleView, BulkConfirmView,
    PlannedVehicleView, BulkDispatchView,
    DispatchedVehicleView, BulkCompletedView,
    )

app_name = 'delivery'

urlpatterns = [
    path('assigning/<int:pk>/update_order/', UpdateSortOrderView.as_view(), name='update_sort_order'),
    path('status_update/<int:pk>/<str:status>/', StatusUpdateView.as_view(), name='status_update'),
    path('vehicles/', VehicleListView.as_view(), name='vehicle_list'),
    path('vehicles/create/', VehicleCreateView.as_view(), name='vehicle_create'),
    path('vehicle/<int:pk>/update/', VehicleUpdateView.as_view(), name='vehicle_update'),
    path('vehicle/<int:pk>/delete/', VehicleDeleteView.as_view(), name='vehicle_delete'),
    path('vehicle/<int:pk>/assigning/dates/', AssigningDateListView.as_view(), name='assigning_date_list'),
    path('vehicle/<int:pk>/assigning/', AssigningVehicleView.as_view(), name='assigning_vehicle_list'),
    path('vehicle/<int:pk>/assigning/bulk_confirm/', BulkConfirmView.as_view(), name='bulk_confirm'),
    path('vehicle/<int:pk>/planned/', PlannedVehicleView.as_view(), name='planned_vehicle_list'),
    path('vehicle/<int:pk>/planned/bulk_dispatch/', BulkDispatchView.as_view(), name='bulk_dispatch'),
    path('vehicle/<int:pk>/dispatched/', DispatchedVehicleView.as_view(), name='dispatched_vehicle_list'),
    path('vehicle/<int:pk>/dispatched/bulk_completed/', BulkCompletedView.as_view(), name='bulk_completed'),
    path('unassigned/', UnassignedListView.as_view(), name='unassigned_list'),
    path('bulk_assign/', BulkAssignView.as_view(), name='bulk_assign'),
]