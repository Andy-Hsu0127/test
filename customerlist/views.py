from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer
from .forms import CustomerForm
from django import forms
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .resources import CustomerResource
from tablib import Dataset
from django.views import View
import logging

@login_required
def customer_list(request):
    # 獲取 'search' 參數，如果不存在則為空字串
    search_query = request.GET.get('search', '').strip()
    
    # 獲取 'sort' 和 'order' 參數，設置默認值
    sort = request.GET.get('sort', 'customer_code')  # 默認按客戶代碼排序
    order = request.GET.get('order', 'asc')  # 默認升序
    
    # 定義可排序的欄位，這裡僅允許 'customer_code'
    valid_sort_fields = ['customer_code']
    
    if sort not in valid_sort_fields:
        sort = 'customer_code'  # 如果排序欄位無效，使用默認欄位
    
    if order == 'desc':
        sort_field = f'-{sort}'
    else:
        sort_field = sort  # 默認升序
    
    # 根據搜尋條件過濾客戶
    if search_query:
        customers = Customer.objects.filter(
            Q(customer_name__icontains=search_query) |
            Q(customer_code__icontains=search_query) |
            Q(unified_number__icontains=search_query) |
            Q(contact_person__icontains=search_query) |
            Q(contact_phone__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(out_address__icontains=search_query)
        ).order_by(sort_field)
    else:
        customers = Customer.objects.all().order_by(sort_field)
    
    # 設定每頁顯示的客戶數量，例如每頁 10 筆
    paginator = Paginator(customers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'customers': page_obj,  # 模板中迭代的對象
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'paginator': paginator,
        # 傳遞當前的排序和搜索參數
        'current_sort': sort,
        'current_order': order,
        'search_query': search_query,
    }
    
    return render(request, 'customerlist/customer_list.html', context)

@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()
            return redirect('customerlist:customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customerlist/customer_form.html', {'form': form, 'title': '新增客戶'})

@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customerlist:customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customerlist/customer_form.html', {'form': form, 'title': '編輯客戶'})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customerlist:customer_list')
    return render(request, 'customerlist/customer_confirm_delete.html', {'customer': customer})



class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['created_by']
        fields = [
            'customer_name', 
            'customer_code', 
            'unified_number',
            'contact_person',
            'contact_phone',
            'email',
            'out_address',
            'created_by',
            ]  # 根據你的模型調整字段

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


#import excel

logger = logging.getLogger(__name__)

class ImportCustomersView(View):
    def post(self, request, *args, **kwargs):
        customer_resource = CustomerResource()
        dataset = Dataset()
        import_file = request.FILES.get('import_file')

        if not import_file:
            messages.error(request, '未選擇任何文件進行匯入。')
            return redirect('customerlist:customer_list')

        try:
            # 確認文件格式
            file_format = import_file.name.split('.')[-1].lower()
            if file_format not in ['xls', 'xlsx']:
                messages.error(request, '不支援的文件格式。請上傳 Excel (.xlsx) 文件。')
                return redirect('customerlist:customer_list')

            # 加載數據
            imported_data = dataset.load(import_file.read(), format=file_format)

            # Dry run 驗證
            result = customer_resource.import_data(imported_data, dry_run=True)

            if not result.has_errors():
                # 實際匯入
                customer_resource.import_data(imported_data, dry_run=False)
                messages.success(request, '客戶資料匯入成功！')
            else:
                error_messages = []
                for error in result.row_errors():
                    error_messages.append(f"第 {error.row + 1} 行錯誤：{error.error}")

                for error in result.dataset_errors():
                    error_messages.append(f"資料錯誤：{error}")

                messages.error(request, '匯入過程中出現錯誤，請檢查文件格式和數據。')
                for msg in error_messages:
                    messages.error(request, msg)
        except Exception as e:
            logger.error(f'匯入失敗：{e}', exc_info=True)
            messages.error(request, f'匯入失敗：{e}')

        return redirect('customerlist:customer_list')