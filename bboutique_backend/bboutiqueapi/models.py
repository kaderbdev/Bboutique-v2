
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
import uuid

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

class Guest(models.Model):
    guest_id = models.UUIDField( default=uuid.uuid4 ,unique=True,editable=False)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return str(self.guest_id)
    


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
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True ,blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    storage = models.PositiveIntegerField(default=0)
    condition = models.CharField(max_length=50, blank=True, null=True)
    material = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='product_variants/', blank=True, null=True)


    def __str__(self):
        variant_info = [f"Color: {self.color}", f"Size: {self.size}", f"Price: {self.price}", f"Stock: {self.stock}", f"Storage: {self.storage}", f"Condition: {self.condition}", f"Material: {self.material}"]
        return f"{self.product.name} - " + " - ".join(filter(None, variant_info))


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart' ,null=True,blank=True)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='cart' ,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def items(self):
        return self.items.all()
    @property
    def total(self):
        return sum(item.total_price for item in self.items.all())
    def __str__(self):
        if self.user:
            return f"Cart of {self.user.username}"
        else:
            return f"Cart of {self.guest.guest_id}"
    
    

class CartItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(default=1)
    @property
    def total_price(self):
        return self.product.base_price * self.quantity
    def __str__(self):
        if self.cart.user:
            return f"{self.quantity} x {self.product.name} in {self.cart.user}'s cart"
        else:
            return f"{self.quantity} x {self.product.name} in {self.cart.guest}'s cart"
            