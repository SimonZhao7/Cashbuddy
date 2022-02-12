from django.db import models
from account.models import CustomUser
from categories.models import Category

# Create your models here.

class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=200, decimal_places=2)
    description = models.CharField(max_length=1000, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_created = models.DateTimeField()
    
    def get_slug(self):
        return self.pk + 205324952

    @staticmethod
    def get_id(slug):
        return int(slug) - 205324952
    
    def __str__(self):
        return "{}: {}".format(self.user, self.title)