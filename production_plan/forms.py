from django import forms
from django.forms import inlineformset_factory
from .models import Product, ProductProcess, OrderItemProcess, OrderItem

OrderItemProcessFormSet = inlineformset_factory(
    OrderItem,
    OrderItemProcess,
    fields=['planned_start'],
    extra=0,
    widgets={
        'planned_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    }
)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'code', 'name', 'location',
            'slid_size', 'flow_direction',
            'length', 'width', 'height',
            'area', 'flute_type',
        ]

class ProductProcessForm(forms.ModelForm):
    class Meta:
        model = ProductProcess
        fields = ['process', 'sequence']

class OrderItemProcessForm(forms.ModelForm):
    class Meta:
        model = OrderItemProcess
        fields = ['planned_start']
        widgets = {
            'planned_start': forms.DateInput(attrs={'type': 'date'}),
        }

