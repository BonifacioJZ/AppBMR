from rest_framework import serializers
from src.product.models import Product
from src.pay.models import Pay,PayDetails

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name')

class PayDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)
    sub_total = serializers.SerializerMethodField(method_name="total")
    class Meta:
        model = PayDetails
        fields = ('id','product','quantity','price','sub_total')
        
    def total(self,pay_detail:PayDetails)->float:
        return pay_detail.price * pay_detail.quantity

class PaySerializer(serializers.ModelSerializer):
    details = PayDetailSerializer(many=True,read_only=True)
    total = serializers.SerializerMethodField(method_name="cal_total")
    
    class Meta:
        model = Pay
        fields = ('id','total_items','details','date','total')
    
    def cal_total(self,pay:Pay)->float:
        total = 0 
        pay_details = PayDetails.objects.filter(pay=pay)
        for pay_d in pay_details:
            total = total +(pay_d.quantity * pay_d.price)
        return total
    
    