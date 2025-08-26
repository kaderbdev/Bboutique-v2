from django.contrib import admin
from .models import CustomUser, client, Vendor,Product,Category,CartItem,Cart,Guest,ProductVariant
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(client)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Vendor)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Guest)
admin.site.register(ProductVariant)
