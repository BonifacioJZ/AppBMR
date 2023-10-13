import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from src.cart.models import Cart

"""The UserAccountManager class is responsible for creating user accounts and superuser accounts,
    including setting their email, password, and additional fields, and saving them to the database.
    """
class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()
        
        shopping_cart = Cart.objects.create(user=user)
        shopping_cart.save()
        
        return user

    
    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=150,unique=True,null=False,blank=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name','email']

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email