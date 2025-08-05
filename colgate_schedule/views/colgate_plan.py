from webbrowser import get
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, UpdateView
from ..models import OrderItemProcess, ColgateScheduleItem
from production_plan.models import Process
from datetime import datetime, date

# メニュー用ビュー
class ColgateMenuView(LoginRequiredMixin, TemplateView):
    template_name = 'colgate_schedule/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today()
        return context


class ColgateProcessSchedule(LoginRequiredMixin, View):
    template_name = 'colgate_schedule/colgate_schedule.html'
    
    def get(self, request, date_str, flute):
        # URLパラメータのdate_str引数を日付型に変換
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return render(request, '404.html', status=404)
        # コルゲート工程を特定（コードや名前は実務に合わせて変更）
        col_process = get_object_or_404(Process, code='0101')
        # 対象データ取得
        processes = OrderItemProcess.objects.filter(
            process=col_process,
            planned_start=target_date,
            status='planning',
            order_item__product__flute_type=flute,
        ).select_related(
            'order_item__product',
        ).order_by(
            'display_order',
        )
        # 製品情報を初期表示用にまとめる
        schedule_items = []
        for process in processes:
            # 既存がなければ自動作成
            item, created = ColgateScheduleItem.objects.get_or_create(process=process)
            print(created)
            if created:
                item.save()  # 初回はsave()で貼合m計算
            schedule_items.append(item)
        
        context = {
            'target_date': target_date,
            'flute': flute,
            'schedule_items': schedule_items,
        }

        return render(request, self.template_name, context)

# 計画詳細
class ColgateScheduleDetail(LoginRequiredMixin, UpdateView):
    model = ColgateScheduleItem
    template_name = 'colgate_schedule/colgate_schedule_detail.html'
    fields = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        schedule_item = self.object
        order_item = schedule_item.order_item_process.order_item
        product = order_item.product

        context['order_item'] = order_item
        context['product'] = product
        
        return context