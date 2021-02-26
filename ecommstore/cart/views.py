from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from temp.decorators import consumer_required
from .cart import Cart
from .forms import CheckOutForm
from .models import CartProducts
# Create your views here.

def cart_detail(request):
    cart = Cart(request)

    in_cart =  CartProducts


    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)

        return redirect('cart')

    if change_quantity:
        cart.add(change_quantity, quantity, True)

        return redirect('cart')

    return render(request, 'cart.html')


@login_required
@consumer_required
def checkout(request):
    cart = Cart(request)
    total_cost = cart.get_total_cost()
    if request.method == "POST":
        form = CheckOutForm
        if form.is_valid():
            Cart(request).clear()
            return redirect('successpage')

    form = CheckOutForm
    return render(request, 'checkout.html', {'cost': total_cost, 'form':form})