#Django Imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
#Local Imports
from src.category.models import Category
from src.category.serializers import CategorySerializer,CategoryDetailsSerializer
# The CategoryCreateListView class is used to either list all categories or create a new category.
class CategoryCreateListView(ListCreateAPIView):
    """The CategoryCreateListView class is used to either list all categories or create a new category.


    Args:
        ListCreateAPIView (_type_): List to categories
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# The above class defines two API views for retrieving and updating category objects, with appropriate
# permissions and serialization.
class CategoryRetrieveAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Category.objects.select_related().all()
    serializer_class = CategoryDetailsSerializer

# The `CategoryUpdateAPIView` class is a view that allows authenticated users to update a category
# object using the PUT method.
class CategoryUpdateAPIView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    
    def get_queryset(self,pk=None):
        return self.get_serializer().Meta.model.objects.all().filter(pk=pk).first()
    def put(self, request, pk=None, *args, **kwargs):
        """
        The `put` function updates a category object with the provided data if it exists, and returns
        the updated data or any validation errors.
        
        :param request: The `request` parameter is an object that represents the HTTP request made by
        the client. It contains information such as the request method (e.g., GET, POST), headers, query
        parameters, and the request body
        :param pk: The "pk" parameter is used to identify a specific object in the database. It stands
        for "primary key" and is typically an integer or a unique identifier for the object. In this
        case, it is used to retrieve a specific object from the queryset
        :return: The code is returning a Response object with the serialized data if it is valid, along
        with a status code of 200 (OK). If the data is not valid, it returns a Response object with the
        serializer errors and a status code of 400 (BAD_REQUEST).
        """
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
        """
        The above function deletes an object with the specified primary key if it exists, and returns a
        response indicating success or failure.
        
        :param request: The `request` parameter is an object that represents the HTTP request made by the
        client. It contains information such as the request method (GET, POST, etc.), headers, query
        parameters, and the request body. It is used to retrieve information from the client and perform
        actions based on that information
        :param pk: The "pk" parameter stands for "primary key". It is used to identify a specific object
        in the database. In this case, it is used to identify the object that needs to be deleted
        :return: The code is returning a Response object with a message "destroy" and a status code of
        204 (NO_CONTENT) if the queryset with the given primary key (pk) exists and is successfully
        deleted. If the queryset does not exist, it returns a Response object with a status code of 404
        (NOT_FOUND).
        """
        if self.get_queryset(pk):
            self.get_queryset(pk).delete()
            return Response({"message","destroy"},status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)