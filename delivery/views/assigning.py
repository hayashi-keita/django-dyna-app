from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from ..models import DeliverySchedule
import json

# 並び替え更新
class UpdateSortOrderView(LoginRequiredMixin, View):
    def post(self, request, pk):
        data = json.loads(request.body.decode('utf-8'))
        for item in data:
            DeliverySchedule.objects.filter(
                pk=item['pk']).update(sort_order=item['sort_order'])
        return JsonResponse({'status': 'ok'})