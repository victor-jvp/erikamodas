from .models import Product, TransactionCab, TransactionDet, CustomUser
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "location")


class CustomUserAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")

class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'stock']


class EditProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name']


class TransactionForm(ModelForm):
    class Meta:
        model = TransactionDet
        fields = ['cab', 'type', 'product', 'amount']
    # def save(self, *args, **kwargs):
        
