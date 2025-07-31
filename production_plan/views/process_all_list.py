from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views import View
from django.shortcuts import get_object_or_404, render
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


class CompleteProcessListView(LoginRequiredMixin, View):
    def get(self, request, pk, scheduled_date):
        process = get_object_or_404(Process, pk=pk)
        schedules = (
            OrderItemProcess.objects
            .filter(process__pk=pk, planned_start=scheduled_date, status='complete')
            .select_related('order_item__order', 'order_item__product', 'process')
            .order_by('display_order', 'pk')
        )
        return render(request, 'production_plan/complete_process_list.html', {
            'process': process,
            'schedules': schedules,
            'scheduled_date': scheduled_date,
        })

