from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from production_plan.models import OrderItemProcess
from ..services.process_expansion import expand_process_for_order_item
from orders.models import OrderItem
from django.contrib import messages


class OrderItemProcessCreateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order_item = get_object_or_404(OrderItem, pk=pk)
        process = order_item.processes.filter(status='pending')
        process.update(status='draft')

        return redirect('production_plan:orderitem_process_list_all')

# 一括工程展開
class ExpandAllOrderItemProcessView(LoginRequiredMixin, View):
    def post(self, request):
        # 未展開の注文商品を取得
        order_item_process = OrderItemProcess.objects.filter(status='pending')
        order_item_process.update(status='draft')
    
        return redirect('production_plan:orderitem_process_list_all')
