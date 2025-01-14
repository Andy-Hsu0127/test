from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    customer_name = models.CharField(max_length=255, verbose_name='客戶')
    customer_code = models.CharField(max_length=100, unique=True, verbose_name='代碼')
    unified_number = models.CharField(max_length=50, unique=True, verbose_name='統一編號',blank=True,null=True)
    contact_person = models.CharField(max_length=255, verbose_name='聯絡人',blank=True,null=True)
    contact_phone = models.CharField(max_length=20, verbose_name='連絡電話',blank=True,null=True)
    email = models.EmailField(unique=True, verbose_name='Email',blank=True,null=True )
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='創建人',blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='創建時間',blank=True,null=True)
    out_address = models.CharField(max_length=255, verbose_name='送貨地',blank=True,null=True)

    def __str__(self):
        return self.customer_name

    class Meta:
        ordering = ['-created_at']
        verbose_name = '客戶'
        verbose_name_plural = '客戶列表'
