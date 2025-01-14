from django.contrib import admin
from .models import Inventory

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('vendor_part_number', 'customer', 'total_quantity', 'inventory_quantity', 'created_by', 'created_at')
    search_fields = ('vendor_part_number', 'customer__customer_name')
    list_filter = ('customer', 'created_at')
