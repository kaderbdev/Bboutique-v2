from django.shortcuts import render,get_object_or_404
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import viewsets
from .models import CustomUser,client, Vendor,Product,Category,Cart,CartItem,Guest
from rest_framework.authtoken.models import Token
from .serializers import ProductSerializer,VendorSerilizer,CategorySerializer,VendorSerializer2,CategorySerialize2,CartSerializer,CartItemSerializer,CustumUserSerializer,GuestSerilizer
# Create your views here.

@api_view(['POST'])
def user_loogin(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')

    except:
        return Response({'masage':'Fields given dont match'})
    user = get_object_or_404(CustomUser,username=username)


    if user:
        if check_password(password,user.password):
            token,created = Token.objects.get_or_create(user=user)
            serializer = CustumUserSerializer(user)
            return Response({"message": "User logged in successfully", "token": token.key,'data':serializer.data}, status=201)
        else:
            return Response({"message": "incorrect password"}, status=201)





@api_view(['POST'])
def user_registration(request):
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        
    except:
        return Response({'message':'Fields given dont match'})
    if password1 != password2:
        return Response({"error": "Passwords do not match"}, status=400)
    if CustomUser.objects.filter(username=username).exists() :
        return Response({"error": "Username already exists"}, status=400)
    user = CustomUser.objects.create_user(username=username, password=password1,email=email)
    user.save()
    client.objects.create(user=user)   # Create a client profile for the user
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = CustumUserSerializer(user)
    return Response({"message": "User registered successfully", "token": token.key,'data':serializer.data}, status=201)



@api_view(['POST','GET'])
@permission_classes([AllowAny])
def cart_display(request):
    cart = None
    if request.user.is_authenticated:
        user = request.user
        cart,created = Cart.objects.get_or_create(user=user) # Get or create a cart for the user
    elif request.query_params.get('guest_id')or request.data.get('guest_id')or request.COOKIES.get('guest_id'):
         print('hh')
         
         guest_id = request.query_params.get('guest_id')
         guest = get_object_or_404(Guest,guest_id = guest_id)
         cart_guest,_ = Cart.objects.get_or_create(guest=guest)
         if cart is not None:
            for item in cart_guest.items.all():
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=item.product)
                if not created:
                    cart_item.quantity =item.quantity
                    cart_item.save()
                    
                else:
                    cart_item.quantity = item.quantity
                    cart_item.save()
                    
                
         else:
              cart = cart_guest
    else:
         return Response({'error':'an error ocured'},status=404)


   
    if request.method == 'POST':
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        
        product = get_object_or_404(Product,id = product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity =quantity
            cart_item.save()
            return Response({"message": "Item quantity updated in cart"}, status=200)
        else:
            cart_item.quantity = quantity
            cart_item.save()
            return Response({"message": "Item added to cart"}, status=201)
    if request.method == 'GET': 
      
        serializer = CartSerializer(cart)
        return Response({'data': serializer.data}, status=200)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    serializer = CustumUserSerializer(user)
    return Response({'data': serializer.data}, status=200)



@api_view(['POST'])
def guest_create(request):
     guest = Guest.objects.get_or_create()
     serializer = GuestSerilizer(guest)
     return Response({'data':serializer.data})
     


class ProductViewset(viewsets.ModelViewSet):
    queryset =Product.objects.all()
    serializer_class = ProductSerializer




class VendorViewset(viewsets.ModelViewSet):
        queryset =Vendor.objects.all()
        serializer_class = VendorSerializer2


class CategoryViewset(viewsets.ModelViewSet):
        queryset =Category.objects.all()
        serializer_class = CategorySerialize2

class CartViewset(viewsets.ModelViewSet):
        queryset =Cart.objects.all()
        serializer_class = CartSerializer
        
        
        

