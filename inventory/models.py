from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
       verbose_name_plural = 'categories'


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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TransactionType(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=-1)
    
    def __str__(self):
        return self.name
    

class TransactionCab(models.Model):
    date = models.DateField()
    comment = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Transaction(models.Model):
    cab_id = models.ForeignKey(TransactionCab, models.CASCADE)
    type = models.ForeignKey(TransactionType, on_delete=models.RESTRICT)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    amount = models.FloatField()
