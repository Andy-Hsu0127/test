from django import forms
from .models import Inventory

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['vendor_part_number', 'customer', 'total_quantity', 'notes', 'inventory_quantity']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
