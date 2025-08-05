from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from ..models import ColgateScheduleItem

@require_POST
def update_take_count(request):
    import json
    data = json.loads(request.body.decode('utf-8'))
    item_pk = data.get('item_pk')
    take_count = int(data.get('take_count', 1))

    item = get_object_or_404(ColgateScheduleItem, pk=item_pk)
    item.take_count = take_count
    item.save()  # 貼合m再計算

    return JsonResponse({
        'planned_m': str(item.planned_m),
        'is_reversed': item.is_reversed,
    })

@require_POST
def update_detail(request):
    pk = request.POST.get('item_pk')
    item = get_object_or_404(ColgateScheduleItem, pk=pk)
    # 数量と取数
    quantity = request.POST.get('quantity')
    take_count = request.POST.get('take_count')
    if quantity:
        item.order_item_process.order_item.quantity = int(quantity)
        item.order_item_process.order_item.save()
    if take_count:
        item.take_count = int(take_count)
    
    # 紙巾・材質
    paper = item.order_item_process.order_item.product
    paper.width = request.POST.get('width') or paper.width
    