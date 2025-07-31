from unittest.util import sorted_list_difference
from django.db import models
from django.contrib.auth.models import User

# 拠点
class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name='拠点名')

    def __str__(self):
        return self.name

# 顧客
class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name='得意先名')
    code = models.CharField(max_length=20, unique=True, verbose_name='得意先コード')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.code} - {self.name}'

# 届先
class DeliveryDestinaion(models.Model):
    name = models.CharField(max_length=100, verbose_name='届先名')
    code = models.CharField(max_length=10, unique=True, verbose_name='届先コード')
    customer =models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='得意先')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='拠点')
    
    def __str__(self):
        return f'{self.code} - {self.name}'

# 製品
class Product(models.Model):

    FLUTE_TYPE_CHOICES = [
        ('A', 'A段'),
        ('B', 'B段'),
        ('C', 'C段'),
        ('V', 'V段'),
        ('W', 'W段'),
        ('E', 'E段'),
        ('G', 'G段')
    ]

    name = models.CharField(max_length=100, verbose_name='製品名')
    code = models.CharField(max_length=20, unique=True, verbose_name='製品コード')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='拠点')
    slid_size = models.CharField(max_length=50, verbose_name='スリッタ寸法', null=True, blank=True)
    flow_direction = models.CharField(max_length=50, verbose_name='流れ寸法', null=True, blank=True)
    length = models.DecimalField(max_digits=6, decimal_places=1, verbose_name='完成寸法（縦）', null=True, blank=True)
    width = models.DecimalField(max_digits=6, decimal_places=1, verbose_name='完成寸法（横）', null=True, blank=True)
    height = models.DecimalField(max_digits=6, decimal_places=1, verbose_name='完成寸法（高さ）', null=True, blank=True)
    area = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='平米', null=True, blank=True)
    flute_type = models.CharField(max_length=10, choices=FLUTE_TYPE_CHOICES, verbose_name='フルート', null=True, blank=True)

    def __str__(self):
        return f'{self.code} - {self.name}'

# 受注
class Order(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='得意先')
    delivery = models.ForeignKey(DeliveryDestinaion, on_delete=models.CASCADE, verbose_name='届先')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='所属拠点')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    order_number = models.CharField(max_length=20, unique=True, verbose_name='受注No')

    def __str__(self):
        return self.order_number

# 注文明細
class OrderItem(models.Model):

    ORDER_TYPE_CHOICES = [
        ('normal', '通常受注'),
        ('forecast', '見込受注'),
        ('confirmed', '出荷確定'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    customer_order_number = models.CharField(max_length=20, verbose_name='注文No')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='製品名')
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES, default='normal', verbose_name='受注区分')
    delivery_date = models.DateField(null=True, blank=True, verbose_name='納期')
    delivery_time = models.TimeField(null=True, blank=True, verbose_name='納入時間')
    quantity = models.PositiveIntegerField(verbose_name='数量')


    def __str__(self):
        return f'{self.product.name} × {self.quantity} (注文No：{self.customer_order_number})'

# ユーザー拡張(拠点ごとに紐づく)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username