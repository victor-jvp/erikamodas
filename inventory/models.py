from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Location(models.Model):
    name = models.CharField(max_length=255)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    pass
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=255)
    stock = models.IntegerField()
    # CASCADE: elimina el producto
    # PROTECT: lanza un error
    # RESTRICT: Solo elimina sino existen productos
    # SET_NULL: actualiza a valor nulo
    # SET_DEFAULT: asigna valor por defecto
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TransactionCab(models.Model):
    date = models.DateField()
    location = models.ForeignKey(Location, models.RESTRICT)
    comment = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)


class TransactionDet(models.Model):
    cab = models.ForeignKey(TransactionCab, models.CASCADE)
    type = models.CharField(max_length=3)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    amount = models.FloatField()
