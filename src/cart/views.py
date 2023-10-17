from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction
from src.cart.models import Cart,CartItem
from src.product.models import Product
from src.cart.serializers import CartSerializer
# Create your views here.

class CartApiView(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        """Get all products in to cart and the total price
        """
        
        user = self.request.user
        cart = Cart.objects.get(user=user)
        result = CartSerializer(cart)
        
        return Response(result.data,status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        """Add item to cart or one more if it already exists
        """
        data = request.data
        user = request.user
        cart = Cart.objects.get(user=user)
        
        if not data.get('product'):
            return Response({'error':'the product is required'})
        
        if not Product.objects.filter(id=data.get('product')).exists():
            return Response({'error':'the product id not exist'})
        
        product = Product.objects.get(id=data.get('product'))
        price = product.price
        
        if not data.get('count'):
            count = 1
        else:
            count = data.get('count')
        
        with transaction.atomic():
            try:
                if CartItem.objects.filter(cart=cart, product=product).exists():
                    cart.total_items += count
                    cart.total = cart.total + (price*count) 
                    cart_item = CartItem.objects.filter(cart=cart, product=product).get()
                    cart_item.quantity += count
                    cart_item.save()
                    cart.save()
                    return Response({'success':'added'},status=status.HTTP_200_OK)
        
                cart.total_items += count
        
                CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity =count
                ).save()
                cart.save()
                return Response({'success':'added'},status=status.HTTP_200_OK) 
            except Exception as e:
                print(e)
                return Response({'error':'error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    
        
class CartUpdateAndDeleteApiView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def put(self, request, pk=None, *args, **kwargs):
        """update quality of cart
        """
        user = request.user
        data = request.data
        
        if not Product.objects.filter(id=pk).exists():
            return Response({'error':'the product is not exist'},status=status.HTTP_404_NOT_FOUND)
        
        product = Product.objects.get(id=pk)
        cart = Cart.objects.get(user=user)
        
        if not CartItem.objects.filter(cart=cart,product=product).exists():
            return Response({'error':'the product is not exist it to the cart'},status=status.HTTP_404_NOT_FOUND)
        
        item = CartItem.objects.filter(cart=cart,product=product).get()
        quantity = item.quantity
        if not data.get('count'):
            
            item.quantity = quantity + 1
            cart.total_items = cart.total_items + 1
            cart.total = cart.total + (product.price*1)
            
            cart.save()
            item.save()
            
            return Response({"message":"Updated"},status=status.HTTP_200_OK)
        
        count = data.get('count')
        item.quantity = quantity + count
        cart.total_items = cart.total_items + count
        
        cart.save()
        item.save()
        return Response({"message":"Updated"},status=status.HTTP_200_OK)
        
    def delete(self, request,pk=None,*args,**kwargs):
        """Remove product to cart """
        user = request.user
        cart = Cart.objects.get(user=user)
        
        if not Product.objects.filter(pk=pk).exists():
            return Response({"message":"Product not exit"}, status=status.HTTP_404_NOT_FOUND)
        product = Product.objects.get(pk=pk)
        
        if not CartItem.objects.filter(product=product,cart=cart).exists():
            return Response({"message":"the product not exists in to cart"},status=status.HTTP_404_NOT_FOUND)
        
        item = CartItem.objects.get(product=product, cart=cart)
        quantity = item.quantity
        
        item.delete()
        
        cart.total_items = cart.total_items - quantity
        cart.save()
        
        return Response({"message":"Item Deleted"},status=status.HTTP_200_OK)
        
        