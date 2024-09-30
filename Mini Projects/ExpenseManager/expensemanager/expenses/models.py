from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


# Create your models here.
class Expense(models.Model):
    amount = models.DecimalField(max_digits=100,decimal_places=2)
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User,on_delete=models.CASCADE)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category

    class Meta:
        ordering:['-date']

class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name