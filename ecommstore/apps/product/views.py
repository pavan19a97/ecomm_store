from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from apps.product.forms import AddToCartForm
from apps.product.models import Product
from apps.cart.models import CartProducts
from apps.cart.cart import Cart

# Create your views here.
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

            messages.success(request, 'The product was added to the cart')

            return redirect('product', category_slug=category_slug, product_slug=product_slug)
    else:
        form = AddToCartForm()
    similar_products = list(product.category.products.exclude(id = product.id))
    return render(request, 'products/product.html', {'form':form, 'product':product,'similar_products': similar_products})
