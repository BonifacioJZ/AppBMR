#Python Imports
import uuid
#Django Imports
from django.db import models
from django.urls import reverse
#Local Import
from src.category.models import Category

# Create your models here.
class Product(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name = models.CharField(max_length=150,blank=False,null=False)
    desc = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10,decimal_places=2,blank=False,null=False)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, null=False, blank=False,related_name='category',verbose_name='Category',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural ="Products"

    def __str__(self):
        return self.name
