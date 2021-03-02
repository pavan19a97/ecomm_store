from django.contrib.auth.forms import UserCreationForm
from django.forms import models, Form, IntegerField
from .models import User
from apps.product.models import Product

class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'avatar','is_vendor', 'is_consumer', 'password1', 'password2']


