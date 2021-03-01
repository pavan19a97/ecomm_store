from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserForm, ProductForm, AddToCartForm
from django.contrib.auth import forms
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.db.models import Q
from django.core.paginator import Paginator
from .decorators import  consumer_required, vendor_required
from .models import Product,User, Category
from cart.models import CartProducts
from cart.cart import Cart


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

def product(request, category_slug, product_slug):
    cart = Cart(request)
    product = get_object_or_404(Product, category__slug = category_slug, slug =  product_slug)
    if request.method == 'POST':
        form = AddToCartForm(request.POST)

        if form.is_valid():

            quantity = form.cleaned_data['quantity']
            if request.user.is_authenticated:

                queryy = CartProducts.objects.filter(cartUser=request.user, cartProduct=product)
                print(len(queryy))
                if len(queryy) == 0:
                    cartpro = CartProducts(cartUser=request.user, cartProduct=product, quantity=quantity)
                    cartpro.save()
                else:
                    queryy[0].quantity +=1
                    queryy[0].save()

                cart.add(product_id=product.id, quantity=quantity, update_quantity=False)
            else:
                cart.add(product_id=product.id, quantity=quantity, update_quantity=False)

            # cart = CartProducts.objects.filter(cartUser=request.user)
            # for item in cart:
            #     print(item.id, item.cartProduct, item.cartUser)
            # for p in cart:
            #     cart1 = Product.objects.get(title=p.cartProduct)
            #     print(cart1)
            # for p in cart:
            #     cart[str(p)]['product'] = Product.objects.get(title=p)
            #
            # print(sum(item['quantity'] * item['product'].price for item in cart.values()))


            messages.success(request, 'The product was added to the cart')

            return redirect('product', category_slug=category_slug, product_slug=product_slug)
    else:
        form = AddToCartForm()
    similar_products = list(product.category.products.exclude(id = product.id))
    return render(request, 'products/product.html', {'form':form, 'product':product,'similar_products': similar_products})

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

