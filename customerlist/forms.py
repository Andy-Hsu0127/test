from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'customer_name',
            'customer_code',
            'unified_number',
            'contact_person',
            'contact_phone',
            'email',
            'out_address',
        ]
