from django.db import models
from django.contrib.auth.models import User
from orders.models import Product, OrderItem

# 工程マスタ
class Process(models.Model):
    name = models.CharField(max_length=100, verbose_name='工程名')
    code = models.CharField(max_length=20, verbose_name='工程コード')

    def __str__(self):
        return f'{self.code} - {self.name}'

# 製品工程マスタ
class ProductProcess(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_process')
    process = models.ForeignKey(Process, on_delete=models.CASCADE, verbose_name='工程名')
    sequence = models.PositiveIntegerField(verbose_name='工程順序')

    class Meta:
        unique_together = ('product', 'sequence')
        ordering = ['sequence']
    
    def __str__(self):
        return f'{self.product.code} - {self.sequence} - {self.process.name}'

# 受注明細ごとの工程展開
class OrderItemProcess(models.Model):
    STATUS_CHOICES = [
        ('pending', '未展開'),
        ('draft', '予定作成'),
        ('planning', '差立中'),
        ('complete', '指示作成'),
    ]
    
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='processes')
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    sequence = models.PositiveIntegerField()
    planned_start = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='ステータス')
    is_completed = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0, verbose_name='表示順')  # 並び順

    class Meta:
        ordering = ['sequence']
    
    def __str__(self):
        return f'{self.order_item} - {self.sequence} - {self.process.name}'

