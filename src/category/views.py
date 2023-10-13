#Django Imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
#Local Imports
from src.category.models import Category
from src.category.serializers import CategorySerializer,CategoryDetailsSerializer
class CategoryCreateListView(ListCreateAPIView):
    """List all categories or Create a new category

    Args:
        ListCreateAPIView (_type_): List to categories
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryRetrieveAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Category.objects.select_related().all()
    serializer_class = CategoryDetailsSerializer

class CategoryUpdateAPIView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    
    def get_queryset(self,pk=None):
        return self.get_serializer().Meta.model.objects.all().filter(pk=pk).first()
    def put(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            category_serializer = self.serializer_class(self.get_queryset(pk),data=request.data)
            if category_serializer.is_valid():
                category_serializer.save()
                return Response(category_serializer.data,status=status.HTTP_200_OK)
            return Response(category_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class CategoryDestroyApiView(DestroyAPIView):
    """Destroy category 
    Returns:
        _type_: Delete category to data base
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    
    def get_queryset(self,pk=None):
        return self.get_serializer().Meta.model.objects.all().filter(pk=pk).first()
    def delete(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            self.get_queryset(pk).delete()
            return Response({"message","destroy"},status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)