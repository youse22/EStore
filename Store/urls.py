"""
URL configuration for Store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.contrib import admin
from django.urls import path

from Estore.views import add_to_cart, cart_page, checkout, confirmation_page, create_account, error_page, home, login, product_page, product_search, remove_from_cart, update_cart

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', home, name='home'),
    path('create_account/', create_account, name='create_account'),
    path('', login, name='login'),
    # path('logout/', logout_view, name='logout'),
    path('products/', product_page, name='product_page'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_page, name='cart_page'),
    path('update_cart/<int:product_id>/', update_cart, name='update_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('confirmation/', confirmation_page, name='confirmation_page'),
    path('error/<str:error_code>/', error_page, name='error_page'),
    path('product-search/', product_search, name='product_search'),
]




    

