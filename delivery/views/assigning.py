from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from ..models import DeliverySchedule, Vehicle
import json

# 並び替え更新
class UpdateSortOrderView(LoginRequiredMixin, View):
    def post(self, request, pk):
        data = json.loads(request.body.decode('utf-8'))
        for item in data:
            DeliverySchedule.objects.filter(
                pk=item['pk']).update(sort_order=item['sort_order'])
        return JsonResponse({'status': 'ok'})

# 車両ごとの配車中日付一覧
class AssigningDateListView(LoginRequiredMixin, View):
    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk, is_active=True)
        # 配車中の DeliverySchedule から日付一覧を取得
        schedule_dates = (
            DeliverySchedule.objects
            .filter(vehicle=vehicle, status='assigning')
            .exclude(delivery_date__isnull=True)
            .values_list('delivery_date', flat=True)
            .distinct()
            .order_by('delivery_date')
        )
        
        return render(request, 'delivery/assigning_date_list.html', {
            'vehicle': vehicle,
            'schedule_dates': schedule_dates,
        })

