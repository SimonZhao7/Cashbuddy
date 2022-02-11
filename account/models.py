from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField()
    budget = models.DecimalField(max_digits=250, decimal_places=2, default=0)
