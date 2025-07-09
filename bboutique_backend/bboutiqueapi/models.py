from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
 



class CustomUser(AbstractUser):
    usertype_choices = (
        ('admin', 'Admin'),
        ('client', 'client'),
        ('vendor', 'Vendor'),
    )
    usertype = models.CharField(max_length=10, choices=usertype_choices, default='client')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)




class client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client_profile')

    def __str__(self):
        return self.user.username

class Vendor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='vendor_profile')
    shop_name = models.CharField(max_length=100, default=None)
    Shop_profile_picture = models.ImageField(upload_to='vendor_profile_pictures/', blank=True, null=True)
    shop_description = models.TextField(blank=True, null=True)
    


    def __str__(self):
        return self.shop_name

class admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='admin_profile')
    admin_level = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.user.username
    












class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name




class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def items(self):
        return self.items.all()
    @property
    def total(self):
        return sum(item.total_price for item in self.items.all())
    def __str__(self):
        return f"Cart of {self.user.username}"
    
    

class CartItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(default=1)
    @property
    def total_price(self):
        return self.product.price * self.quantity
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"
    