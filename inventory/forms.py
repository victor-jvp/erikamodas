from . import models
from django.forms import ModelForm


class CreateProductForm(ModelForm):
    class Meta:
        model = models.Product
        fields = ['name', 'category', 'stock']


class EditProductForm(ModelForm):
    class Meta:
        model = models.Product
        fields = ['name', 'category']


class TransactionForm(ModelForm):
    class Meta:
        model = models.Transaction
        fields = ['cab_id', 'type', 'product', 'amount']
    # def save(self, *args, **kwargs):
        
