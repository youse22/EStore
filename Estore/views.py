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
        cart[product_id] = new_quantity  
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
        client_id = '481f4da5a814079ab9cddd2a6435efc8'
        client_secret = 'oHrr4tbnB1PH0uz6VQNUve6i4a2aTk99VKjprl1AdE_HmynTAKY5M8pZRU7V--Pv'
        moncash = moncashify.API(client_id, client_secret)
        print('hello')
        payment = moncash.payment(order_id, total_price)
        print("hel")
        print(payment)
        return redirect(payment.redirect_url)
    else:
        return render(request, 'checkout.html', {'order_id': order_id, 'total_price': total_price})



def confirmation_page(request):
    return render(request, 'confirmation_page.html')

def error_page(request, error_code):
    error = ErrorPage.objects.get(error_code=error_code)
    return render(request, 'error_page.html', {'error': error})


from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
import tensorflow as tf
from PIL import Image 

# Charger le modèle pré-entraîné pour l'extraction de caractéristiques
model = tf.keras.applications.MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

def extract_features(image):
    # Prétraitement de l'image
    img = image.resize((224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array[tf.newaxis,...])

    # Extraction des caractéristiques
    features = model.predict(img_array)

    return features

def product_search(request):
    if request.method == 'POST':
        uploaded_image = request.FILES.get('image')
        query = request.POST.get('query')

        if uploaded_image:
            # Traitez l'image téléchargée pour extraire ses caractéristiques visuelles
            image = Image.open(uploaded_image)
            features = extract_features(image)

            # Comparez les caractéristiques de l'image avec celles de vos produits dans la base de données
            # Recherchez des produits similaires
            # Renvoyez les résultats à une page de résultats de recherche
            image_results = None  # Remplacer par la logique de recherche par image
        else:
            image_results = None

        if query:
            # Recherchez les produits correspondant à la requête de l'utilisateur
            name_results = Product.objects.filter(name__icontains=query)
        else:
            name_results = None

        return render(request, 'search_results.html', {'image_results': image_results, 'name_results': name_results, 'query': query})

    return HttpResponse("Méthode non autorisée", status=405)
