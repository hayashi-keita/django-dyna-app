from django.db import models
from production_plan.models import OrderItemProcess, Product

# 原紙マスタ
class ProductPaper(models.Model):
    LAYER_CHOICES = [
        ('face', '表'),
        ('medium', '中芯'),
        ('liner', '裏'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='papers')
    layer = models.CharField(max_length=20, choices=LAYER_CHOICES, verbose_name='層')
    paper_type = models.CharField(max_length=50, verbose_name='原紙銘柄')
    basis_wight = models.PositiveIntegerField(null=True, blank=True, verbose_name='坪量(g/m2)')
    slit_width = models.DecimalField(max_digits=6, decimal_places=1, verbose_name='紙巾(mm)', null=True, blank=True)
    display_order = models.PositiveIntegerField(default=0, verbose_name='表示順')

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f'{self.product.code} - {self.get_layer_display()} - {self.paper_type}'

# 貼合m計算
class ColgateScheduleItem(models.Model):
    order_item_process = models.ForeignKey(OrderItemProcess, on_delete=models.CASCADE, related_name='clgate_items')
    take_count = models.PositiveIntegerField(default=1, verbose_name='取数(丁取り)')
    trim = models.PositiveIntegerField(default=0, verbose_name='トリム(mm)')
    planned_m = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='貼合ｍ')
    is_reversed = models.BooleanField(default=False, verbose_name='反転')
    # 計画ごとの紙巾・材質（初期値はProductからコピー）
    paper_width = models

    class Meta:
        ordering = ['order_item_process__display_order']
    
    def cal_planned_m(self):
        """貼合m = (流れ寸法 × 数量) / 取数"""
        product = self.order_item_process.order_item.product
        if not product.flow_direction or not self.take_count:
            return 0
        return (float(product.flow_direction) * self.order_item_process.order_item.quantity) / self.take_count
    
    def save(self, *args, **kwargs):
        # 保存時に自動保存
        self.planned_m = self.cal_planned_m()
        # 400m未満は反転
        self.is_reversed = (self.planned_m < 400)
        super().save(*args, **kwargs)