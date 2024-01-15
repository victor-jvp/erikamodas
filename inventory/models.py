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
    

class TransactionType(models.Model):
    name = models.CharField(max_length=3)
    isActive = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class TransactionCab(models.Model):
    date = models.DateField()
    comment = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    
    class Meta:
        db_table="transactions_cab"


class TransactionDet(models.Model):
    cab = models.ForeignKey(TransactionCab, related_name="details", on_delete=models.CASCADE)
    type = models.ForeignKey(TransactionType, on_delete=models.RESTRICT)
    location = models.ForeignKey(Location, models.RESTRICT)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    amount = models.FloatField()
    
    class Meta:
        db_table = "transactions_det"
