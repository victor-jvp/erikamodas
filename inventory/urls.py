from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('<int:product_id>', views.details, name='details'),
    path('<int:product_id>/edit', views.edit, name='edit'),
    path('transactions/', views.transaction_index, name='transaction_index'),
    path('ajax/transactions', views.ajax_transactions, name='ajax_transactions')
]
