#Python Import
#Django Import
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
#Local Import
from src.product.serializers import ProductSerializer,ProductDetailSerializer
# The `ProductListCreateApiView` class is a view that allows listing or creating products, with the
# ability to retrieve all products or create a new product.
class ProductListCreateApiView(ListCreateAPIView):
    """The `ProductListCreateApiView` class is a view that allows listing or creating products, with the
ability to retrieve all products or create a new product.

    Returns:
        _type_: list all products or new product
    """
    serializer_class = ProductSerializer
    permission_classes=(IsAuthenticatedOrReadOnly,)
    
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    
# The `ProductRetrieveApiView` class is a view that retrieves a product and returns it in a product
# detail view.
class ProductRetrieveApiView(RetrieveAPIView):
    """ The `ProductRetrieveApiView` class is a view that retrieves a product and returns it in a product
detail view.

    Returns:
        _type_: return to product detail view
    """
    permission_classes= (IsAuthenticatedOrReadOnly,)
    serializer_class = ProductDetailSerializer
    
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all().prefetch_related()
    

class ProductUpdateApiView(UpdateAPIView):
    """ The `put` function updates the information of a product using the provided request data.
        
        :param request: The `request` parameter is an object that contains information about the current
        HTTP request. It includes details such as the request method (GET, POST, PUT, DELETE), headers,
        query parameters, and the request body
        :param pk: The "pk" parameter stands for "primary key" and is used to identify a specific object
        in the database. In this case, it is used to identify the product that needs to be updated
        :return: The code is returning a Response object with the serialized data of the updated product
        if the serializer is valid. The status code returned is HTTP_200_OK. If the serializer is not
        valid, it returns a Response object with the serializer errors and a status code of
        HTTP_400_BAD_REQUEST.
    Returns:
        _type_: return the product updated
    """
    permission_classes=(IsAuthenticated,)
    serializer_class = ProductSerializer
    
    def get_queryset(self,pk=None):
        return self.serializer_class.Meta.model.objects.all().filter(pk=pk).first()
    
    def put(self, request,pk=None, *args, **kwargs):
        """
        The `put` function updates the information of a product using the provided request data.
        
        :param request: The `request` parameter is an object that contains information about the current
        HTTP request. It includes details such as the request method (GET, POST, PUT, DELETE), headers,
        query parameters, and the request body
        :param pk: The "pk" parameter stands for "primary key" and is used to identify a specific object
        in the database. In this case, it is used to identify the product that needs to be updated
        :return: The code is returning a Response object with the serialized data of the updated product
        if the serializer is valid. The status code returned is HTTP_200_OK. If the serializer is not
        valid, it returns a Response object with the serializer errors and a status code of
        HTTP_400_BAD_REQUEST.
        """
        # The code block is responsible for updating the information of a product.
        if self.get_queryset(pk):
            serializer = self.serializer_class(self.get_queryset(pk),data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ProductDestroyApiView(DestroyAPIView):
    """he above function deletes an object with the specified primary key if it exists, and returns a
        response indicating success or failure.
        
        :param request: The `request` parameter is an object that represents the HTTP request made by the
        client. It contains information such as the request method, headers, body, and query parameters.
        It is used to retrieve information from the request or perform actions based on the request
        :param pk: The "pk" parameter stands for "primary key". It is used to identify a specific object
        in the database. In this case, it is used to identify the object that needs to be deleted
        :return: The code is returning a response with a message "deleted" and a status code of 204
        (NO_CONTENT) if the queryset with the given primary key (pk) exists and is successfully deleted.
        If the queryset does not exist, it returns a response with a status code of 404 (NOT_FOUND).
    Returns:
        _type_: return message to success
    """
    serializer_class= ProductSerializer 
    
    def get_queryset(self,pk=None):
        return self.get_serializer().Meta.model.objects.all().filter(pk=pk).first()
    
    def delete(self, request,pk=None, *args, **kwargs):
        """
        The above function deletes an object with the specified primary key if it exists, and returns a
        response indicating success or failure.
        
        :param request: The `request` parameter is an object that represents the HTTP request made by the
        client. It contains information such as the request method, headers, body, and query parameters.
        It is used to retrieve information from the request or perform actions based on the request
        :param pk: The "pk" parameter stands for "primary key". It is used to identify a specific object
        in the database. In this case, it is used to identify the object that needs to be deleted
        :return: The code is returning a response with a message "deleted" and a status code of 204
        (NO_CONTENT) if the queryset with the given primary key (pk) exists and is successfully deleted.
        If the queryset does not exist, it returns a response with a status code of 404 (NOT_FOUND).
        """
        if self.get_queryset(pk):
            self.get_queryset(pk).delete()
            return Response({"message":"deleted"},status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)