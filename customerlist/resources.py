# customers/resources.py

from import_export import resources, fields
from .models import Customer

class CustomerResource(resources.ModelResource):
    customer_name = fields.Field(column_name='customer_name', attribute='name')
    customer_code = fields.Field(column_name='customer_code', attribute='code')
    unified_number = fields.Field(column_name='unified_number', attribute='unified_number')
    contact_person = fields.Field(column_name='contact_person', attribute='contact_person')
    contact_phone = fields.Field(column_name='contact_phone', attribute='contact_phone')
    EMAIL = fields.Field(column_name='EMAIL', attribute='email')
    out_address = fields.Field(column_name='out_address', attribute='out_address')
    created_at = fields.Field(column_name='created_at', attribute='created_at')
    created_by = fields.Field(column_name='created_by', attribute='created_by')

    class Meta:
        model = Customer
        import_id_fields = ('email',)  # 使用 email 作為唯一標識
        fields = ('customer_name', 'customer_code', 'unified_number', 'contact_person', 'contact_phone', 'EMAIL', 'created_at', 'created_by')
        skip_unchanged = True
        report_skipped = True
