#Django Imports
from rest_framework import serializers
#Local Imports
from src.category.models import Category
from src.product.models import Product
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name','desc')
        
class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name','price','is_active')

class CategoryDetailsSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(many=True,read_only=True)
    class Meta:
        model = Category
        fields = ('id','name','desc','category')