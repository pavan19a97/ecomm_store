from django.db import models
from apps.core.models import User, Product
# Create your models here.

class CartProducts(models.Model):
    cartUser = models.ForeignKey(User, on_delete=models.CASCADE, blank = True)
    cartProduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()