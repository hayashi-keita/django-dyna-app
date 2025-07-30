from django import forms
from .models import Order, OrderItem

# 受注フォーム（ヘッダー）
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'delivery']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'order_type', 'delivery_date', 'delivery_time', 'customer_order_number']

        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
            'delivery_time': forms.TimeInput(attrs={'type': 'time'}),
        }

