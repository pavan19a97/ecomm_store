from django.contrib.auth.forms import UserCreationForm
from django.forms import models, Form, IntegerField

from apps.product.models import Product

class ProductForm(models.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['vendor']
