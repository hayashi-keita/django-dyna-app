from django.views import View
from django.shortcuts import redirect, get_object_or_404
from ..models import DeliverySchedule
from django.contrib.auth.mixins import LoginRequiredMixin

# 配送ステータス更新処理
class StatusUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk, status):
        schedule = get_object_or_404(DeliverySchedule, pk=pk)

        valid_statuses = ['planned', 'dispatched', 'completed']
        if status in valid_statuses:
            schedule.status = status
            schedule.save()
        # 前のページに戻る（なければ未配車リストへ）    
        return redirect(request.META.get('HTTP_REFERER', 'delivery:unassigned_list'))

        