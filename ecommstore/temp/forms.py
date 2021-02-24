from django.contrib.auth.forms import UserCreationForm
from django.forms import models, Form, IntegerField
from .models import User, Product

class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'avatar','is_vendor', 'is_consumer', 'password1', 'password2']
class ProductForm(models.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['vendor']

class AddToCartForm(Form):
    quantity = IntegerField()
