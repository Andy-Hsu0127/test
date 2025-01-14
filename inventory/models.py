from django.db import models
from django.contrib.auth.models import User
from customerlist.models import Customer  # 替換 'your_app' 為包含 Customer 模型的應用程式名稱

class Inventory(models.Model):
    vendor_part_number = models.CharField(max_length=100, verbose_name='廠商料號')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='客戶名稱')
    total_quantity = models.PositiveIntegerField(verbose_name='總數量')
    inventory_quantity = models.PositiveIntegerField(verbose_name='庫存數量')
    notes = models.TextField(blank=True, null=True, verbose_name='備註')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='創建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')

    def __str__(self):
        return f"{self.vendor_part_number} - {self.customer.customer_name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = '庫存'
        verbose_name_plural = '庫存管理'
