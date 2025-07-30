from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from ..forms import ProductForm, ProductProcessForm
from ..models import Product, ProductProcess

class ProductCreateView(LoginRequiredMixin, View):
    def get(self, request):
        product_form = ProductForm()
        ProductProcessFormSet = inlineformset_factory(
            Product,
            ProductProcess,
            form=ProductProcessForm,
            extra=10,
            can_delete=False,
        )
        formset = ProductProcessFormSet()

        return render(request, 'production_plan/product_create.html', {
            'product_form': product_form,
            'formset': formset,
        })
    
    def post(self, request):
        product_form = ProductForm(request.POST)
        ProductProcessFormSet = inlineformset_factory(
            Product,
            ProductProcess,
            form=ProductProcessForm,
            extra=10,
            can_delete=False,
        )

        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.location =request.user.userprofile.location
            product.save()

            formset = ProductProcessFormSet(request.POST, instance=product)
            if formset.is_valid():
                formset.save()
                return redirect('production_plan:product_success')
        
        return render(request, 'production_plan/product_create.html', {
            'product_form': product_form,
            'formset': formset,
        })