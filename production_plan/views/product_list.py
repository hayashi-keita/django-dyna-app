from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Product
from django.db.models import Q

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'production_plan/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(code__icontains=query) | Q(name__icontains=query)
            )
        return queryset