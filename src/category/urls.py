"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from src.category.views import CategoryDestroyApiView, CategoryCreateListView,CategoryRetrieveAPIView,CategoryUpdateAPIView
urlpatterns = [
    path('',CategoryCreateListView.as_view(),name='category_create_list'),
    path('<str:pk>',CategoryRetrieveAPIView.as_view(),name='category_retrieve'),
    path('update/<str:pk>',CategoryUpdateAPIView.as_view(),name='category_update'),
    path('destroy/<str:pk>',CategoryDestroyApiView.as_view(),name='category_destroy'),
]
