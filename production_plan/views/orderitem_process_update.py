from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from ..models import OrderItem, OrderItemProcess, Process
from ..forms import OrderItemProcessFormSet

# 作業日設定
class OrderItemProcessPlanView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order_item = get_object_or_404(OrderItem, pk=pk)
        formset = OrderItemProcessFormSet(instance=order_item)
        return render(request, 'production_plan/orderitem_process_plan.html', {
            'order_item': order_item,
            'formset': formset,
        })
    
    def post(self, request, pk):
        order_item = get_object_or_404(OrderItem, pk=pk)
        formset = OrderItemProcessFormSet(request.POST, instance=order_item)
        
        if formset.is_valid():
            processes = formset.save(commit=False)
            for p in processes:
                if p.planned_start:
                    p.status = 'planning'
                else:
                    p.status = 'draft'
                p.save()
                    
            return redirect('production_plan:orderitem_process_list_all')
        
        return render(request, 'production_plan/orderitem_process_plan.html', {
            'order_item': order_item,
            'formset': formset,
        })

# 工程別の作業日一覧
class ProcessDateListView(LoginRequiredMixin, View):
    def get(self, request, pk):
        process = get_object_or_404(Process, pk=pk)
        # OrderItemProcessから日付一覧を取得
        scheduled_dates = (
            OrderItemProcess.objects
            .filter(process=process)
            .exclude(status='pending')  # 未着手は除外
            .exclude(planned_start__isnull=True)  # Noneは除外
            .values_list('planned_start', flat=True)
            .distinct()
            .order_by('planned_start')
        )
        return render(request, 'production_plan/process_date_list.html', {
            'process': process,
            'scheduled_dates': scheduled_dates,
        })

# 作業日ごとのスケジュール（並び替え可能）
class ScheduleByProcessDateView(LoginRequiredMixin, View):
    def get(self, request, pk, scheduled_date):
        process = get_object_or_404(Process, pk=pk)
        schedules = (
            OrderItemProcess.objects
            .filter(process__pk=pk, planned_start=scheduled_date, status='planning')
            .select_related('order_item__order', 'order_item__product', 'process')
            .order_by('display_order', 'id')
        )
        return render(request, 'production_plan/schedule_by_process_date.html', {
            'schedules': schedules,
            'scheduled_date': scheduled_date,
            'process': process,
        })
    
    def post(self, request, pk, scheduled_date):
        schedule_pks = request.POST.getlist('pks')
        for spk in schedule_pks:
            try:
                process = get_object_or_404(OrderItemProcess, pk=pk)
                new_order = int(request.POST.get(f'display_order_{spk}', process.display_order))
                process.display_order = new_order
                process.save()
            except (OrderItemProcess.DoesNotExist, ValueError):
                continue

        return redirect('production_plan:schedule_by_process_date', pk=pk, scheduled_data=scheduled_date)

# ステータス変更処理
class OrderItemProcessStatusUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        process = get_object_or_404(OrderItemProcess, pk=pk)
        if process.status == 'planning':
            process.status = 'draft'
            process.planned_start = None  # ← ここで日付を空にする
            process.save()
            messages.success(request, '差立を外しました。')
        else:
            messages.warning(request, '差立中のみ有効です。')
    
        return redirect('production_plan:orderitem_process_list_all')