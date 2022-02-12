from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField()
    budget = models.DecimalField(max_digits=250, decimal_places=2, default=0)
    
    def get_slug(self):
        return self.pk + 454089658
    
    @staticmethod
    def get_id(slug):
        return int(slug) - 454089658