from rest_framework.authtoken.models import Token
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from datetime import timedelta

from utils.validators import (
    is_valid_phone_number,is_valid_password,is_valid_birth_date
    )
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email,password,phone_number,**extrafields):
        if not email:
            raise ValueError("The email must be set.")
        if not phone_number:
            raise ValueError("The phone number must be set.")
        email = self.normalize_email(email)
        phone_number = is_valid_phone_number(phone_number)
        user = self.model(email = email,phone_number=phone_number,**extrafields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,email,password,phone_number,**extra_fields):
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('status','Admin')
        extra_fields.setdefault('first_name','Esmatullah')
        extra_fields.setdefault('last_name','Hadel')
        extra_fields.setdefault('country','Af')
        extra_fields.setdefault('city','kabul')

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email,password,phone_number,**extra_fields)
    
class CustomUser(AbstractBaseUser,PermissionsMixin):
    CHOICE = (
        ("Admin",'Admin'),
        ('Editor','Editor'),
        ('Authore','Authore'),
        ('User','User')
    )
    status = models.CharField(max_length=50,default='User',choices=CHOICE)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100,unique=True)
    first_name = models.CharField(max_length=100,blank=True)
    last_name = models.CharField(max_length=100,blank=True)
    picture = models.ImageField(upload_to="images/profile",blank=True)
    address = models.CharField(max_length=100,blank=True)
    country = CountryField(blank=True)
    city = models.CharField(max_length=100,blank=True)
    phone_number = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=255)
    birth_date = models.DateField()
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login_ip = models.GenericIPAddressField(null=True,blank=True)
    last_login = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','phone_number']

    objects = UserManager()
 
    def clean(self):
        if not is_valid_password(self.password):
            raise ValidationError("the password must contain uppercase and lowercase letter and character and number.")
        if not is_valid_birth_date(self.birth_date):
            raise ValidationError("your birth date must be correct.")
        
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

        if not hasattr(self,'profile'):
            Profile.objects.create(user = self)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='profile')
    is_enable = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class Auth_Token(Token):
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        expiration_time = self.created_at + timezone.timedelta(days=30)
        return timezone.now() > expiration_time
    
    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Token"