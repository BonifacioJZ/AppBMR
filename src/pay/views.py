from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from datetime import datetime

from src.cart.models import Cart,CartItem
from src.pay.models import Pay,PayDetails

class PayApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request)->Response:
        """make the sale of the products

        Args:
            request (_type_): user authenticated

        Returns:
            Response: return message with status ok and save sale to save on data base 
        """
        user = request.user
        cart = Cart.objects.get(user=user)
        total_items = cart.total_items
        if not CartItem.objects.filter(cart=cart).exists():
            return Response({'message':'cart is empty'},status=status.HTTP_400_BAD_REQUEST)
        items = CartItem.objects.filter(cart=cart)
        with transaction.atomic():
            try:
                pay = Pay.objects.create(user=user,total_items=total_items,date= datetime.now())
                pay.save()
                for item in items:
                    PayDetails.objects.create(pay=pay,product=item.product,price=item.product.price,quantity=item.quantity).save()
                items.delete()
                cart.total_items = 0
                cart.save()
            except Exception as e:
                print(e)
                return Response({'message':'error making sale'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({'message':'sale made successfully'},status=status.HTTP_200_OK)

    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def put(self, request):
        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        return Response(status=status.HTTP_200_OK)