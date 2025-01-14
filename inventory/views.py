from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import InventoryForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Inventory, Customer  # 確保導入 Customer 模型
from django.shortcuts import render
from django.core.paginator import Paginator

class InventoryListView(ListView):
    model = Inventory
    template_name = 'inventory/inventory_list.html'
    context_object_name = 'inventories'
    paginate_by = 10  # 根據需要調整每頁顯示數量

    def get_queryset(self):
        queryset = super().get_queryset()
        vendor_part_number = self.request.GET.get('vendor_part_number', '').strip()
        customer_id = self.request.GET.get('customer_id', '').strip()

        if vendor_part_number:
            queryset = queryset.filter(vendor_part_number__icontains=vendor_part_number)
        if customer_id:
            queryset = queryset.filter(customer__id=customer_id)
        
        return queryset.select_related('customer').order_by('vendor_part_number')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = Customer.objects.all().order_by('customer_name')  # 傳遞客戶列表
        # 保留現有的搜尋條件以便在模板中使用
        context['selected_customer_id'] = self.request.GET.get('customer_id', '')
        context['vendor_part_number'] = self.request.GET.get('vendor_part_number', '')
        return context

class InventoryDetailView(LoginRequiredMixin, DetailView):
    model = Inventory
    template_name = 'inventory/inventory_detail.html'
    context_object_name = 'inventory'

class InventoryCreateView(LoginRequiredMixin, CreateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'inventory/inventory_form.html'
    success_url = reverse_lazy('inventory:inventory_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class InventoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'inventory/inventory_form.html'
    success_url = reverse_lazy('inventory:inventory_list')

class InventoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Inventory
    template_name = 'inventory/inventory_confirm_delete.html'
    success_url = reverse_lazy('inventory:inventory_list')


def inventory_list(request):
    vendor_part_number = request.GET.get('vendor_part_number', '').strip()
    customer_id = request.GET.get('customer_id', '').strip()

    inventories = Inventory.objects.all().select_related('customer')

    if vendor_part_number:
        inventories = inventories.filter(vendor_part_number__icontains=vendor_part_number)
    if customer_id:
        inventories = inventories.filter(customer__id=customer_id)

    inventories = inventories.order_by('vendor_part_number')

    paginator = Paginator(inventories, 10)  # 每頁顯示 10 條
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    customers = Customer.objects.all().order_by('customer_name')  # 獲取所有客戶

    context = {
        'inventories': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
        'customers': customers,  # 傳遞客戶列表
        'selected_customer_id': customer_id,  # 保留選中的客戶
        'vendor_part_number': vendor_part_number,  # 保留搜尋廠商料號
    }

    return render(request, 'inventory/inventory_list.html', context)

