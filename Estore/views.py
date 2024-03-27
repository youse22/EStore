# views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import ErrorPage, Order, Product
import moncashify

from django.db.models import Sum
from django.contrib.auth import login as auth_login  

def home(request):
    return render(request, 'home.html')

def create_account(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'create_account.html', {'form': form})



def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)  
                return redirect('product_page')  
        else:
            form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')

def product_page(request):
    products = Product.objects.all()
    return render(request, 'product_page.html', {'products': products})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if 'cart' not in request.session:
        request.session['cart'] = []
    cart = request.session['cart']
    cart.append(product.id)
    request.session['cart'] = cart
    return redirect('product_page')

def cart_page(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    product_quantities = {}
    for product_id in cart:
        product_quantities[product_id] = product_quantities.get(product_id, 0) + 1
    for product_id, quantity in product_quantities.items():
        product = Product.objects.get(id=product_id)
        total_price += quantity * product.price
        cart_items.append({'product': product, 'quantity': quantity, 'total_price': float(quantity * product.price)})  # Convertir en float
    total_price = float(total_price)
    request.session['total_price'] = total_price

    return render(request, 'cart_page.html', {'cart_items': cart_items, 'total_price': total_price})

def update_cart(request, product_id):
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity'))
        cart = request.session.get('cart', {})
        cart[str(product_id)] = new_quantity
        request.session['cart'] = cart
    return redirect('cart_page')

def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            del cart[str(product_id)]
            request.session['cart'] = cart
    return redirect('cart_page')



def checkout(request):
    user = request.user
    total_price = request.session.get('total_price')
    print(total_price)
    if total_price is None:
        return HttpResponse("Le montant total n'a pas été récupéré correctement.")

    if request.method == 'POST':
        order_id='es001'
        client_id = ' 481f4da5a814079ab9cddd2a6435efc8'
        client_secret = 'oHrr4tbnB1PH0uz6VQNUve6i4a2aTk99VKjprl1AdE_HmynTAKY5M8pZRU7V--Pv'
        moncash = moncashify.API(client_id, client_secret)
        print('hello')
        payment = moncash.payment(order_id, total_price)
        print("hel")
        print(payment)
        return payment.get_redirect_url()
    else:
        return render(request, 'checkout.html', {'order_id': order_id, 'total_price': total_price})



def confirmation_page(request):
    order_id = request.session.get('order_id')
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return render(request, 'error_page.html', {'error_message': 'Order not found'})
    return render(request, 'confirmation_page.html', {'order': order})

def error_page(request, error_code):
    error = ErrorPage.objects.get(error_code=error_code)
    return render(request, 'error_page.html', {'error': error})
