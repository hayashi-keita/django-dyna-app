from django.views.generic import DetailView
from orders.models import Order, OrderItem

class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = OrderItem.objects.filter(order=self.object)
        return context