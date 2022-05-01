from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
    birthday = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=200)
    phonenumber = models.CharField(max_length=9)

    def __str__(self):
        return self.user.username


class Commodity(models.Model):
    itemName = models.TextField(max_length=200, default='商品尚未上架')
    itemType = models.TextField(max_length=50, default='無')
    price = models.BigIntegerField(default=0)
    quantity = models.BigIntegerField(default=0)
    info = models.TextField(default='無')
    image = models.ImageField(default='static/images/noitem.jpg')
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.itemName
