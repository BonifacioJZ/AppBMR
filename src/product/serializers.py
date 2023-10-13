#Python imports

#Django imports
from rest_framework import serializers
#Local imports
from src.product.models import Product
from src.category.models import Category
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name','desc','price','category','is_active')
        

class CategoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name','desc')
class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategoryProductSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ('id','name','desc','price','category','is_active')