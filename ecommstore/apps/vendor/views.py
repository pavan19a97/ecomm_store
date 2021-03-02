
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

from apps.core.forms import UserForm, ProductForm
from apps.core.decorators import  consumer_required, vendor_required

# Create your views here.

# vendorviews
@login_required
@vendor_required
def vendor_admin(request):
    vendor = request.user
    products = vendor.products.all()

    return render(request, 'vendor/vendor_admin.html',{'vendor':vendor,'products':products})

@login_required
@vendor_required
def add_product(request):
    if request.method == 'POST':
        form= ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor  = request.user
            product.slug = slugify(product.title)
            product.save()
            return redirect('vendor_home')
    else:
        form = ProductForm()
    return render(request, 'vendor/add_product.html',{'form':form})
