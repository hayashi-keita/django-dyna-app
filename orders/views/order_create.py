from calendar import c
from re import I
from django.shortcuts import render, redirect
from django.views import View
from ..forms import OrderForm, OrderItemForm
from ..models import Location, OrderItem, UserProfile,Order
from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin
from production_plan.services.process_expansion import expand_process_for_order_item
from datetime import datetime
import uuid


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        order_form = OrderForm()
        OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=3, can_delete=False)
        formset = OrderItemFormSet()

        return render(request, 'orders/order_create.html',{
            'order_form': order_form,
            'formset': formset,
        })

    def post(self, request):
        order_form =OrderForm(request.POST)

        if order_form.is_valid():
            user_profile = UserProfile.objects.get(user=request.user)
        
            order = order_form.save(commit=False)
            order.created_by = request.user
            order.location = user_profile.location
            # ユニークな受注番号を生成（例：ORD20250724001）
            today_str = datetime.now().strftime('%Y%m&d')
            order_number = f'ORD{today_str}-{uuid.uuid4().hex[:6].upper()}'
            order.order_number = order_number       
            order.save()

            # OrderItemモデルの新しいデータを作成するためのフォームセットを生成
            # extra=3により、3つの空のフォームが追加され、ユーザーが最大3つの新しいOrderItemを一度に作成できる
            OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=3, can_delete=False)
            # queryset=OrderItem.objects.none()を指定することで、既存のデータは表示されず、新規作成専用のフォームセットになる
            formset = OrderItemFormSet(request.POST, instance=order)

            if  formset.is_valid():
                formset.save()
                for item in order.items.all():    
                    # 工程展開
                    expand_process_for_order_item(item)
                return redirect('orders:order_success')
        
        else:
            # フォームが無効な場合でも、FormSetは生成しておく必要
            OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=3, can_delete=False)
            formset = OrderItemFormSet(request.POST)
        
        return render(request, 'orders/order_create.html', {
            'order_form': order_form,
            'formset': formset,
        })

