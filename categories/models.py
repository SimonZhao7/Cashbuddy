from django.db import models
from account.models import CustomUser

# Create your models here.


class Category(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    
    def get_slug(self):
        return self.pk + 562425830

    @staticmethod
    def get_id(slug):
        return int(slug) - 562425830
    
    def __str__(self):
        return "{}: {}".format(self.user, self.name)