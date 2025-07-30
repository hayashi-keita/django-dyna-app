from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from ..models import OrderItemProcess

    
# 工程完了ボタン
class OrderItemProcessCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        process = get_object_or_404(OrderItemProcess, pk=pk)
        if process.status == 'planning':
            process.status = 'completed'
            process.save()
            messages.success(request, '工程を完了に変更しました。')
        
        else:
            messages.warning(request, "完了に変更できるのは'差立中'の工程のみです。")
        
        return redirect('production_plan:orderitem_process_list_all')