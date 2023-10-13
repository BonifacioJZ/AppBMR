from rest_framework import serializers

from src.cart.models import Cart,CartItem
from src.product.models import Product



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name','price')
        
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)
    sub_total = serializers.SerializerMethodField(method_name="total")
    class Meta:
        model = CartItem
        fields = ('id','product','quantity','sub_total')
    
    def total(self, cart_item:CartItem):
        return cart_item.quantity * cart_item.product.price
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,read_only=True)
    sub_total = serializers.SerializerMethodField(method_name="total")
    class Meta:
        model = Cart
        fields = ('id','items','total_items','sub_total')
            
    def total(self,cart:Cart)->float:
        cart_items = CartItem.objects.filter(cart=cart)
        sub_total = 0
        for item in cart_items:
            sub_total = item.product.price * item.quantity
        return sub_total