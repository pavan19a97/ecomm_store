from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.db.models import Q
from django.core.paginator import Paginator

from .forms import UserForm, ProductForm
from .decorators import  consumer_required, vendor_required
from .models import  User, Category
from apps.product.models import Product



# Create your views here.
def filterProducts(min, max, products):

    filteredPro = Product.objects.filter(price__range=(min, max))
    print(filteredPro)
    return filteredPro


def home(request):
    user = request.user
    if user.is_authenticated and user.is_vendor and not user.is_consumer:
        return redirect('vendor_home')

    products = Product.objects.all()

    if request.GET.get('min') and request.GET.get('min'):
        min = request.GET.get('min')
        max = request.GET.get('max')

        products = filterProducts(min, max, products)
    paginator =  Paginator(products, 2)
    # products = paginator.page(2)
    if request.GET.get('page'):
        page_num =  request.GET.get('page')
        products = paginator.page(page_num)
        page_obj = paginator.get_page(page_num)
    else:
        if len(products) > 0:
            products = paginator.page(1)
            page_obj = paginator.get_page(1)
        else:
            products = None
            page_obj = None

    return render(request, "home.html", {'products':products, "paginator": paginator,"page_obj": page_obj, "range": range(1, paginator.num_pages+1)})

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')

            return redirect('ecommstore_home')
    else:
        form = UserForm()
    return render(request, "signup.html", {'u_form': UserForm})




def category(request, category_slug):
    category = get_object_or_404(Category, slug = category_slug)
    return render(request, 'products/category.html', {'category': category})

def search(request):
    query = request.GET.get('query', '')
    print(query)
    products = Product.objects.filter(Q(title__icontains=query)| Q(description__icontains=query))

    # if products == None:
    #     return render(request,'product/search.html', {'products':products,'query': query , 'message':"none"})
    return render(request,'products/search.html', {'products':products,'query': query })

# cart

