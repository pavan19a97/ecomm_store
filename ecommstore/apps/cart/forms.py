from django import forms

class CheckOutForm(forms.Form):
    address1 = forms.CharField()
    address2 = forms.CharField()
    zipcode = forms.IntegerField()
    country = forms.CharField()
    phonenumber = forms.IntegerField()
    debitcardnumber = forms.IntegerField()
    expirydate = forms.IntegerField()
    cvv = forms.IntegerField()
