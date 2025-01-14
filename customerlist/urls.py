from django.urls import path
from . import views
from .views import ImportCustomersView


app_name = 'customerlist'

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('create/', views.customer_create, name='customer_create'),
    path('<int:pk>/edit/', views.customer_update, name='customer_update'),
    path('<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('import/', ImportCustomersView.as_view(), name='import_customers'),
]
