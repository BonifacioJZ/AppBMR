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
        """
        The function calculates the total cost of items in a shopping cart.
        
        :param cart: The "cart" parameter is an instance of the "Cart" class. It represents a shopping
        cart object that contains a collection of items
        :type cart: Cart
        :return: the sub_total, which is the total cost of all the items in the cart.
        """
        cart_items = CartItem.objects.filter(cart=cart)
        sub_total = 0
        for item in cart_items:
            sub_total = sub_total + (item.product.price * item.quantity)
        return sub_total