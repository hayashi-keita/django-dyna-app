from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
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
            order_item__delivery_date=target_date,
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

