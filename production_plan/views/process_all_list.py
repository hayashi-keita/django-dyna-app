from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from ..models import OrderItemProcess, Process


class AllOrderItemProcessListView(LoginRequiredMixin, ListView):
    model =OrderItemProcess
    template_name = 'production_plan/orderitem_process_list_all.html'
    context_object_name = 'processes'
    ordering = ['order_item__order__order_number', 'sequence']

    def get_queryset(self):
        return OrderItemProcess.objects.filter(
            status='draft'
            ).filter(planned_start__isnull=True
            ).select_related(
                'order_item__order',
                'order_item__product',
                'process',
            ).order_by(
            'order_item__order__order_number', 'sequence',
        )

class ProcessListView(LoginRequiredMixin, ListView):
    model = Process
    template_name = 'production_plan/process_list.html'
    context_object_name = 'process'
