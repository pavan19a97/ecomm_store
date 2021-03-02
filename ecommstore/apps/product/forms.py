from django.forms import Form, IntegerField

class AddToCartForm(Form):
    quantity = IntegerField()