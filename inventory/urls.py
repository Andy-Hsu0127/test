# inventory/urls.py
from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.InventoryListView.as_view(), name='inventory_list'),
    path('create/', views.InventoryCreateView.as_view(), name='inventory_create'),
    path('<int:pk>/', views.InventoryDetailView.as_view(), name='inventory_detail'),
    path('<int:pk>/update/', views.InventoryUpdateView.as_view(), name='inventory_update'),
    path('<int:pk>/delete/', views.InventoryDeleteView.as_view(), name='inventory_delete'),
]
