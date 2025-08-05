from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.utils.timezone import now
from ..models import Vehicle, DeliverySchedule
from datetime import datetime

# 未配車リストを「日付・車両選択付き兼配車画面」に改修
class UnassignedListView(LoginRequiredMixin, View):
    def get(self, request):
        # クエリパラメータの日付を取得（なければ今日）
        target_date_str = request.GET.get('date')
        if target_date_str:
            target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()
        else:
            target_date = now().date()
        # 日付で絞り込んだ未配車データ
        schedules = DeliverySchedule.objects.filter(
            status='unassigned',
        ).select_related(
            'order_item__order', 'order_item__product',
        ).order_by('order_item__delivery_date')
        # 稼働中の車両を取得
        vehicles = Vehicle.objects.filter(is_active=True)

        return render(request, 'delivery/unassigned_list.html', {
            'schedules': schedules,
            'vehicles': vehicles,
            'target_date': target_date,
        })

class BulkAssignView(LoginRequiredMixin, View):
    def post(self, request):
        vehicle_pk = request.POST.get('vehicle')
        delivery_date = request.POST.get('delivery_date')
        schedule_pks = request.POST.getlist('schedule_pks')  # 複数取得

        if not (vehicle_pk and delivery_date and schedule_pks):
            messages.warning(request, '車両・日付・注文をすべて選択してください。')
            return redirect('delivery:unassigned_list')
        
        vehicle = get_object_or_404(Vehicle, pk=vehicle_pk)
        DeliverySchedule.objects.filter(
            pk__in=schedule_pks,
            status='unassigned',
        ).update(
            vehicle=vehicle,
            delivery_date=delivery_date,
            status='assigning',
        )
        messages.success(request, f'{len(schedule_pks)}件を{vehicle.vehicle_number}に配車しました。')
        return redirect('delivery:unassigned_list')