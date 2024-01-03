from django.db import models
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    stock = models.IntegerField()
    # puntaje = models.FloatField()

    # CASCADE: elimina el producto
    # PROTECT: lanza un error
    # RESTRICT: Solo elimina sino existen productos
    # SET_NULL: actualiza a valor nulo
    # SET_DEFAULT: asigna valor por defecto
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class TransactionType(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=-1)
    
    def __str__(self):
        return self.name


class Transaction(models.Model):
    date = models.DateField()
    type = models.ForeignKey(TransactionType, on_delete=models.RESTRICT)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
