from django.contrib import admin
from cart import models


class CommodityAdmin(admin.ModelAdmin):
    list_display = ('itemName', 'itemType', 'price', 'quantity')


# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(models.Commodity, CommodityAdmin)


