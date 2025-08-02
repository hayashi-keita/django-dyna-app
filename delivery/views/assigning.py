from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import DeliverySchedule, Vehicle

class AssigningListView(LoginRequiredMixin, View):
    def get(self, request):
        # 配車中（assigning）のみ取得
        schedules = DeliverySchedule.objects.filter(
            status='assigning',
        ).select_related('order_item__order', 'order_item__product')
        # 車両ごとにまとめる
        vehicles = Vehicle.objects.filter(is_active=True)
        vehicle_schedules = []
        for v in vehicles:
            vs = schedules.filter(vehicle=v).order_by(
                'order_item__delivery_date',
                'order_item__delivery_time',
            )
            vehicle_schedules.append((v, vs))

        context = {'vehicle_schedules': vehicle_schedules}
        return render(request, 'delivery/assigning_list.html', context)

# 車両別の配車中一覧
class AssigningVehicleListView(LoginRequiredMixin, View):
    def get(self, request, pk):
        # 車両情報を取得して、配車予定オブジェクトに指定する
        vehicle = get_object_or_404(Vehicle, pk=pk, is_active=True)
        schedules = DeliverySchedule.objects.filter(
            vehicle=vehicle,
            status='assigning',
        ).order_by('sort_order', 'pk')

        return render(request, 'delivery/assigning_vehicle_list.html', {
            'vehicle': vehicle,
            'schedules': schedules,
        })

# 一括配車確定処理
class BulkConfirView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # 車両情報を取得して、配車予定にその車両と配車中をフィルターする
        vehicle = get_object_or_404(Vehicle, pk=pk, is_active=True)
        schedules = DeliverySchedule.objects.filter(
            vehicle=vehicle,
            status='assigning',
        )
        # 配車中から確定にするためステータスをアップデート処理する
        schedules.update(status='planned')
        return redirect('delivery:assigning_vehicle_list', pk=pk)