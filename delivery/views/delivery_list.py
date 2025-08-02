from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.views.generic import ListView
from django.views import View
from django.db.models import Prefetch
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from ..models import DeliverySchedule, Vehicle
from ..forms import AssignVehicleForm

# 未配車リスト
class UnassignedListView(LoginRequiredMixin, ListView):
    model = DeliverySchedule
    template_name = 'delivery/unassigned_list.html'
    context_object_name = 'schedules'
    # 未配車の配車予定だけを取り出す
    def get_queryset(self):
        return DeliverySchedule.objects.filter(
            status='unassigned',
        # 取得した配送データに紐づく注文データ、注文商品データを取得
        ).select_related(
            'order_item__order', 'order_item__product'
        ).order_by(
            # 配送予定を納期順で並び替え
            'order_item__delivery_date',
        )
    # 画面に表示するため、利用可能な車両リストもテンプレートに返す
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicles'] = Vehicle.objects.filter(is_active=True)
        return context

# 車両割当
class AssignVehicleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        schedule = get_object_or_404(DeliverySchedule, pk=pk)
        form = AssignVehicleForm(request.POST, instance=schedule)

        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.status = 'assigning'
            schedule.save()

        return redirect('delivery:unassigned_list')

# 日別配車リスト
class DailyDispatchView(LoginRequiredMixin, View):
    def get(self, request):
        # クエリパラメータの日付を取得
        target_date_str = request.GET.get('date')
        if target_date_str:
            target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()
        else:
            target_date = now().date()
        # 車両ごとに配送予定をまとめる
        vehicles = Vehicle.objects.filter(is_active=True)
        vehicle_schedules = []
        for v in vehicles:
            schedules = DeliverySchedule.objects.filter(
                vehicle=v,
                delivery_date=target_date,
            ).order_by('order_item__delivery_time', 'pk')
            vehicle_schedules.append((v,schedules))
        
        context = {
            'vehicle_schedules': vehicle_schedules,
            'target_date': target_date
        }
        return render(request, 'delivery/daily_dispatch.html', context)