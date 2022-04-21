from django.contrib import admin

from .models import ShopUser, ShopUserProfile

# Register your models here.
admin.site.register(ShopUser)
admin.site.register(ShopUserProfile)
