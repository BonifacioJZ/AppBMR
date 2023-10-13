#Python imports 
import uuid
#Django Imports 
from django.db import models

# Create your models here.

class Category(models.Model):
    id = models.UUIDField(verbose_name="id", default=uuid.uuid4,editable=False, primary_key=True)
    name= models.CharField(max_length=150,blank=False,null=False,unique=True)
    desc = models.CharField(max_length=500,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"
        ordering = ["name"]
    
    
    
