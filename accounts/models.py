from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class User(AbstractUser):
    ACCOUNT_TYPE_CHOICES = (
        ('INVESTOR', 'Investor'),
        ('FARMER', 'Farmer'),
        ('AGENT', 'Agent'),
    )
    
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    other_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=(
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    ))
    phone_number = models.CharField(max_length=12, null=True, blank=True, unique=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    national_id = models.CharField(max_length=50, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phone_number']
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.profile_type = self.account_type
        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Profile(models.Model):
    PROFILE_TYPE_CHOICES = (
        ('INVESTOR', 'Investor'),
        ('FARMER', 'Farmer'),
        ('AGENT', 'Agent'),
    )
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    profile_type = models.CharField(max_length=10, choices=PROFILE_TYPE_CHOICES)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    residential_address = models.CharField(max_length=255, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=11, blank=True)
    account_holder_name = models.CharField(max_length=255, blank=True)
    
    
    
    
    def __str__(self):
        return f"Profile: {self.user.username}"