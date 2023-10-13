import uuid
from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
from src.product.models import Product
# Create your models here.

class Cart(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_items = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    cart = models.ForeignKey(Cart,related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


