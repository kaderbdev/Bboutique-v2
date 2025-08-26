from django.shortcuts import render,get_object_or_404
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view,permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from .models import CustomUser,client, Vendor,Product,Category,Cart,CartItem,Guest,ProductVariant
from rest_framework.authtoken.models import Token
from .serializers import ProductSerializer,VendorSerilizer,CategorySerializer,VendorSerializer2,CategorySerialize2,CartSerializer,CartItemSerializer,CustumUserSerializer,GuestSerilizer,ProductVariantSerializer
# Create your views here.

@api_view(['POST'])
def user_login(request):
    try:
        username = request.data['username']
        password = request.data['password']

    except:
        return Response({'masage':'Fields given dont match'})
    user = get_object_or_404(CustomUser,username=username)


    if user:
        if check_password(password,user.password):
            refresh = RefreshToken.for_user(user)

            serializer = CustumUserSerializer(user)
            response = Response({"message": "User logged in successfully",'data':serializer.data}, status=201)
            response.set_cookie(key='access_token',value=str(refresh.access_token),httponly=True,samesite="Lax")
            response.set_cookie(key="refresh_token",value=str(refresh),httponly=True,samesite="Lax")
            return response
            
            return 
        else:
            return Response({"message": "incorrect password"}, status=201)





@api_view(['POST'])
def user_registration(request):
    try:
        username = request.data['username']
        email = request.data.get('email')
        password1 = request.data['password1']
        password2 = request.data['password2']
       
        
    except:
        return Response({'message':'Fields given dont match'})
    if password1 != password2:
        return Response({"error": "Passwords do not match"}, status=400)
    if CustomUser.objects.filter(username=username).exists() :
        return Response({"error": "Username already exists"}, status=400)
    user = CustomUser.objects.create_user(username=username, password=password1,email=email)
    user.save()
    client.objects.create(user=user)   # Create a client profile for the user
    

    refresh = RefreshToken.for_user(user)

    serializer = CustumUserSerializer(user)
    response = Response({"message": "User registered successfully", 'data':serializer.data}, status=201)
    response.set_cookie(key='access_token',value=str(refresh.access_token),httponly=True,samesite="Lax")
    response.set_cookie(key="refresh_token",value=str(refresh),httponly=True,samesite="Lax")
    return response




class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({"error": "No refresh token"}, status=401)
       
        try:
            refresh = RefreshToken(refresh_token)
            new_access = refresh.access_token
            response = Response({"message": "Token refreshed"})
            response.set_cookie(
                key='access_token',
                value=str(new_access),
                httponly=True,
                samesite='Lax',
                path='/'
            )
            return response
        except Exception:
            return Response({"error": "Invalid refresh token"}, status=401)

@api_view(['POST','GET'])
@permission_classes([AllowAny])
def cart_display(request):
    cart_guest = None
    
    
    guest_id = request.query_params.get('guest_id')or request.data.get('guest_id')or request.COOKIES.get('guest_id')
    if guest_id:
        guest = get_object_or_404(Guest,guest_id = guest_id)
        cart_guest,_ = Cart.objects.get_or_create(guest=guest)
    if request.user.is_authenticated:
        user = request.user
        cart,created = Cart.objects.get_or_create(user=user) # Get or create a cart for the user
        if cart_guest:
            for item in cart_guest.items.all():
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=item.product)

                cart_item.quantity =item.quantity
                item.delete()
                cart_item.save()
                cart.save()
    
        
        


        
                    

                
    else:
            if not guest_id:
                 return Response({'error':"guest_id is required"})
            cart = cart_guest
    


   
    if request.method == 'POST':
        try:
            product_id = request.data['product_id']
            quantity = request.data['quantity']
        except:
            return Response({'message':'Fields given dont match'})
        
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



@api_view(['POST','GET'])
def guest_create(request):
    guest_id = request.query_params.get('guest_id')or request.data.get('guest_id')or request.COOKIES.get('guest_id')
    if not guest_id :
        guest = Guest.objects.create()
        respose = Response({"guest_id":guest.guest_id,})
        respose.set_cookie(key="guest_id",value=str(guest.guest_id),httponly=False,samesite="Lax")
        return respose
    else:
         return Response({'info':'allredy have the guest_id'})


class ProductViewset(viewsets.ModelViewSet):
    queryset =Product.objects.all()
    serializer_class = ProductSerializer


class ProductVariantViewset(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer

class VendorViewset(viewsets.ModelViewSet):
        queryset =Vendor.objects.all()
        serializer_class = VendorSerializer2


class CategoryViewset(viewsets.ModelViewSet):
        queryset =Category.objects.all()
        serializer_class = CategorySerialize2

class CartViewset(viewsets.ModelViewSet):
        queryset =Cart.objects.all()
        serializer_class = CartSerializer
        
        
        

