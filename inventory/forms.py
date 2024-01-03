from . import models
from django.forms import ModelForm


class ProductForm(ModelForm):
    class Meta:
        model = models.Product
        fields = ['name', 'stock', 'category']

class TransactionForm(ModelForm):
    class Meta:
        model = models.Transaction
        fields = ['date', 'type', 'product', 'amount']