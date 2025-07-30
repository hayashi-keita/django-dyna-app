from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import Order, UserProfile

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 20

    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        queryset = Order.objects.filter(location=user_profile.location).order_by('-created_at')

        customer_name = self.request.GET.get('customer')
        if customer_name:
            queryset = queryset.filter(customer__name__icontains=customer_name)
        
        return queryset