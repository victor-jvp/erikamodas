from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Location, Product, CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["username", "email", "location"]
    fieldsets = UserAdmin.fieldsets + (
        (
            'Información de la Tienda',  # you can also use None
            {
                'fields': (
                    'location',
                ),
            },
        ),
    )

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', )


class ProductAdmin(admin.ModelAdmin):
    exclude = ('created_at', )
    list_display = ('name', 'stock', 'created_at')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Product, ProductAdmin)
