from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.utils import timezone



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image_url = models.URLField()

    def __str__(self):
        return self.name

class CartPage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CartPage - User: {self.user}, Total Price: {self.total_price}, Date Created: {self.date_created}"



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    order_id = models.CharField(max_length=50)
    amount = models.FloatField(null=True, blank=True)  # Autoriser les valeurs NULL
    status = models.CharField(max_length=50, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order ID: {self.order_id} - Amount: {self.amount} - Status: {self.status}"

class ErrorPage(models.Model):
    error_code = models.CharField(max_length=10)
    error_message = models.TextField()

    def __str__(self):
        return f"Error {self.error_code}: {self.error_message}" 