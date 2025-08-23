from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import user_registration,ProductViewset,VendorViewset,CategoryViewset,CartViewset,cart_display,user_loogin,user_profile,guest_create


router = DefaultRouter()
router.register('product',ProductViewset,basename='product')
router.register('vendor',VendorViewset,basename='vendor')
router.register('category',CategoryViewset,basename='category')
router.register('cart',CartViewset,basename='cart')

urlpatterns = [
    path('register/', user_registration, name='user_registration'),
    path('loggin/', user_loogin, name='user_loggin'),
    path('cart/', cart_display, name='cart'),
    path('profile/', user_profile, name='user_profile'),
    path('guest/', guest_create, name='guest'),

]+router.urls
