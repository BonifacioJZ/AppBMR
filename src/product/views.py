#Python Import
#Django Import
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
#Local Import
from src.product.serializers import ProductSerializer,ProductDetailSerializer
class ProductListCreateApiView(ListCreateAPIView):
    """List or create products

    Returns:
        _type_: list all products or new product
    """
    serializer_class = ProductSerializer
    permission_classes=(IsAuthenticatedOrReadOnly,)
    
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    
class ProductRetrieveApiView(RetrieveAPIView):
    """Retrieve a product

    Returns:
        _type_: return to product detail view
    """
    permission_classes= (IsAuthenticatedOrReadOnly,)
    serializer_class = ProductDetailSerializer
    
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all().prefetch_related()
    

class ProductUpdateApiView(UpdateAPIView):
    """Update information to product
    Returns:
        _type_: return the product updated
    """
    permission_classes=(IsAuthenticated,)
    serializer_class = ProductSerializer
    
    def get_queryset(self,pk=None):
        return self.serializer_class.Meta.model.objects.all().filter(pk=pk).first()
    
    def put(self, request,pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            serializer = self.serializer_class(self.get_queryset(pk),data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ProductDestroyApiView(DestroyAPIView):
    """Delete a product
    Returns:
        _type_: return message to success
    """
    serializer_class= ProductSerializer 
    
    def get_queryset(self,pk=None):
        return self.get_serializer().Meta.model.objects.all().filter(pk=pk).first()
    
    def delete(self, request,pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            self.get_queryset(pk).delete()
            return Response({"message":"deleted"},status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)