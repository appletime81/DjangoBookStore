from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.
class OrderList(models.Model):
    order_time = models.TextField(default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    user = models.CharField(max_length=150, default='No User')
    product_item = models.TextField(default='No item')
    qty = models.BigIntegerField(default=0)
    price = models.BigIntegerField(default=0)
    paid = models.BooleanField(default=False)
    order_id = models.BigIntegerField(default=0)

    def __str__(self):
        return self.user


class Order(models.Model):
    user = models.CharField(max_length=150, default='No User')
    checkout_time = models.TextField(default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    paid = models.BooleanField(default=False)
