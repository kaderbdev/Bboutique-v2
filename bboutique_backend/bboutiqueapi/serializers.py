from rest_framework.serializers import ModelSerializer
from rest_framework import serializers 
from rest_framework.permissions import IsAuthenticated
from .models import Product,Category,Vendor,Cart,CartItem,CustomUser,Guest









class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class VendorSerilizer(ModelSerializer):

    
    class Meta:
        model = Vendor
        fields = ["shop_name",'id']
     

class GuestSerilizer(ModelSerializer):

    
    class Meta:
        model = Guest
        fields = ["guest_id",'id']
     


class ProductSerializer(ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(queryset = Category.objects.all(),write_only = True,source = 'category')
    vendor_id = serializers.PrimaryKeyRelatedField(queryset = Vendor.objects.all(),write_only = True,source = 'vendor')
    category = CategorySerializer(read_only = True)
    vendor = VendorSerilizer(read_only = True)


    class Meta:
        model = Product
        fields = ['id',
                  'name',
                  'price',
                  'description',
                  'category',
                  'category_id',
                  'vendor',
                  'vendor_id',
                  'image']


class CustumUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','email','usertype','phone_number','address','profile_picture']



class Product_serializer2(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'




class VendorSerializer2(ModelSerializer):

    products = Product_serializer2(many = True,read_only = True)
    user = CustumUserSerializer(read_only = True)
    user_id = serializers.PrimaryKeyRelatedField(queryset = CustomUser.objects.all(),write_only = True,source = 'user')
    class Meta:
        model = Vendor
        fields = ['shop_name','id','products','user','shop_description','Shop_profile_picture','user_id']


class CategorySerialize2(ModelSerializer):
    products = Product_serializer2(many = True,read_only = True)
    
    class Meta:
        model = Category
        fields = '__all__'



# class CartSerializer2(ModelSerializer):
#      class Meta:
#         model = Cart
#         fields = ['user','created_at','updated_at','total']

class CartItemSerializer(ModelSerializer):
    product = Product_serializer2(read_only = True,)
    product_id = serializers.PrimaryKeyRelatedField(queryset = Product.objects.all(),source = 'product')
 
    class Meta:
        model = CartItem
        fields = ['product','quantity','total_price','product_id']



class CartSerializer(ModelSerializer):
    user = CustumUserSerializer(read_only = True)
    user_id = serializers.PrimaryKeyRelatedField(queryset = CustomUser.objects.all(),write_only = True,source= 'user')
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['user','created_at','updated_at','user_id','total','items']




