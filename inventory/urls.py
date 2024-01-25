from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('<int:product_id>', views.details, name='details'),
    path('<int:product_id>/edit', views.edit, name='edit'),
    path('transactions/', views.transaction_index, name='transaction_index'),
    path('transactions/create', views.transaction_create, name='transaction_create'),
    path('ajax/transactions', views.ajax_transactions, name='ajax_transactions'),
    # Locations
    path('locations/', views.location_index, name='location_index'),
    path('locations/create', views.location_create, name='location_create'),
    path('locations/<int:location_id>/edit', views.location_edit, name='location_edit'),
]
