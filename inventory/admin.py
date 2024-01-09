from django.contrib import admin
from .models import Category, Product, Transaction, TransactionType


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


class ProductAdmin(admin.ModelAdmin):
    exclude = ('created_at', )
    list_display = ('name', 'stock', 'created_at')
    
    
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(TransactionType, TransactionTypeAdmin)