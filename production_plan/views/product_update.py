from django.shortcuts import redirect, render, get_object_or_404
from django.forms import inlineformset_factory
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Product, ProductProcess
from ..forms import ProductForm, ProductProcessForm

class ProductUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product_form = ProductForm(instance=product)
        ProductProcessFormSet = inlineformset_factory(
            Product,  # セット元のモデル
            ProductProcess,  # セットするモデル
            form=ProductProcessForm,  # セットするフォームモデル
            extra=10,  # セットするフォームの数
            can_delete=True,  # 削除チェックボタンの有無
        )
        formset = ProductProcessFormSet(instance=product)

        return render(request, 'production_plan/product_update.html', {
            'product_form': product_form,
            'formset': formset,
            'product' : product,
        })
    
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product_form = ProductForm(request.POST, instance=product)
        ProductProcessFormSet = inlineformset_factory(
            Product,
            ProductProcess,
            form=ProductProcessForm,
            extra=10,
            can_delete=True,
        )
        formset = ProductProcessFormSet(request.POST, instance=product)
        
        if product_form.is_valid() and formset.is_valid():
                product_form.save()  # ← product を保存し、インスタンスを取得
                formset.save()
                return redirect('production_plan:product_list')

        return render(request, 'production_plan/product_update.html', {
            'product_form': product_form,
            'formset': formset,
            'product': product,
        }) 