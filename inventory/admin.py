from django.contrib import admin
from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class ProductAdmin(admin.ModelAdmin):
    exclude = ('created_at', )
    list_display = ('id', 'name', 'stock', 'created_at')
# Register your models here.


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
