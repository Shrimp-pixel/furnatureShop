from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.
class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True, verbose_name='аватар')
    age = models.PositiveSmallIntegerField(verbose_name='возраст')

