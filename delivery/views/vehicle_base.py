from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from ..models import Vehicle, DeliverySchedule

class VehicleBaseView(LoginRequiredMixin, View):
    status_filter = None  # サブクラスで指定
    template_name = None  # サブクラスで指定

    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk, is_active=True)
        schedules = DeliverySchedule.objects.filter(
            vehicle=vehicle,
            status=self.status_filter,
        ).select_related(
            'order_item__order', 'order_item__product',
        ).order_by('sort_order', 'pk')

        return render(request, self.template_name, {
            'vehicle': vehicle,
            'schedules': schedules,
        })

# 車両ごとの配車中一覧
class AssigningVehicleView(VehicleBaseView):
    status_filter = 'assigning'
    template_name = 'delivery/assigning_vehicle_list.html'
# 一括配車確定処理
class BulkConfirmView(LoginRequiredMixin, View):
    def post(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk, is_active=True)
        DeliverySchedule.objects.filter(
            vehicle=vehicle,
            status='assigning',
        ).update(status='planned')
        return redirect('delivery:assigning_vehicle_list', pk=pk)

# 車両ごとの配車確定一覧
class PlannedVehicleView(VehicleBaseView):
    template_name = 'delivery/planned_vehicle_list.html'
    status_filter = 'planned'

# 一括出出荷済処理
class BulkDispatchView(LoginRequiredMixin, View):
    def post(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk, is_active=True)
        DeliverySchedule.objects.filter(
            vehicle=vehicle,
            status='planned',
        ).update(status='dispatched')
        return redirect('delivery:planned_vehicle_list', pk=pk)
        
# 車両ごとの出荷済一覧
class DispatchedVehicleView(VehicleBaseView):
    template_name = 'delivery/dispatched_vehicle_list.html'
    status_filter = 'dispatched'
# 一括納品済処理
class BulkCompletedView(LoginRequiredMixin, View):
    def post(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk, is_active=True)
        DeliverySchedule.objects.filter(
            vehicle=vehicle,
            status='dispatched',
        ).update(status='completed')
        return redirect('delivery:dispatched_vehicle_list', pk=pk)