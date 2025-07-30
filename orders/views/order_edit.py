from django.views.generic import UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from orders.models import Order, OrderItem
from orders.forms import OrderForm, OrderItemForm

class OrderUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order_form = OrderForm(instance=order)

        OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=3, can_delete=True)
        formset = OrderItemFormSet(instance=order)

        return render(request, 'orders/order_edit.html', {
            'order_form': order_form,
            'formset': formset,
            'order': order,
        })
    
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order_form = OrderForm(request.POST, instance=order)

        OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=3, can_delete=True)
        formset = OrderItemFormSet(request.POST, instance=order)

        if order_form.is_valid() and formset.is_valid():
            order_form.save()
            formset.save()
            return redirect('orders:order_detail', pk=order.pk)
        
        return render(request, 'orders/order_edit.html', {
            'order_form': order_form,
            'formset': formset,
            'order': order,
        })