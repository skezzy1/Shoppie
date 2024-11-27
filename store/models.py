from django.db import models
from django import forms
from django.contrib.auth.models import User
#Froms models
class Contact(models.Model):
    email = models.EmailField(max_length=255)
    name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Subscribe(models.Model):
    email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.email
    
# Blog model
class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    short_description = models.TextField(max_length=255, blank=True)
    content = models.TextField(max_length=255, blank=False)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
# Product model
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    price = models.FloatField()
    short_description = models.TextField(max_length=50, blank=True)
    content = models.TextField(max_length=255, blank=False)
    image = models.ImageField(upload_to='img/product_images')
    created_at = models.DateTimeField(auto_now_add=True)

    PRODUCT_CATEGORY_CHOICES = [
        (1, 'Choose category'),
        (2, 'Popular'),
        (3, 'Newest'),
        (4, 'Accessories'),
        (5, 'T-shirts'),
        (6, 'Footwear'),
        (7, 'Jackets'),
        (8, 'Others'),
    ]
    product_category = models.IntegerField(choices=PRODUCT_CATEGORY_CHOICES, default=1, blank=False)
    sizes = models.JSONField(verbose_name="Size")
    colors = models.JSONField(verbose_name="Colours")
    
    def __str__(self):
        return self.title

class ProductSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False, label='Search')

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    products = models.ManyToManyField(Product, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f'{self.product.title} ({self.size}) x {self.quantity}'
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=255)
    email = models.EmailField() 
    phone = models.CharField(max_length=20)  
    address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')


    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=10) 

    def __str__(self):
        return f"{self.product.title} ({self.size}) x {self.quantity}"