from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'customer_code', 'unified_number', 'contact_person', 'contact_phone', 'email', 'created_by', 'created_at','out_address']
    search_fields = ['customer_name', 'customer_code', 'unified_number', 'contact_person', 'email','out_address']
    list_filter = ['created_at', 'created_by']
