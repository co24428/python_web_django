from django.db import models

# Create your models here.

class Item(models.Model):
    objects  = models.Manager()

    no      = models.AutoField(primary_key=True)
    name    = models.CharField(max_length=30)
    price   = models.IntegerField(null=True)
    regdate = models.DateField(auto_now_add=True)   