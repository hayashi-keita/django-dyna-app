from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from ..services.process_expansion import expand_process_for_order_item
from orders.models import OrderItem

class OrderItemProcessCreateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order_item = get_object_or_404(OrderItem, pk=pk)
        expand_process_for_order_item(order_item)
        return redirect('production_plan:orderitem_process_list_all')