from django.conf import settings

from django.db import models
from django.contrib.auth.models import User, AbstractUser

import pytz
from datetime import datetime, timedelta


# Create your models here.
class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True, verbose_name='аватар')
    age = models.PositiveSmallIntegerField(verbose_name='возраст', null=True, default=18)

    activate_key = models.CharField(max_length=128, verbose_name='Ключ активации', blank=True, null=True)
    activate_key_expired = models.DateTimeField(blank=True, null=True)

    def is_activate_key_expired(self):
        return datetime.now(pytz.timezone(settings.TIME_ZONE)) > (self.activate_key_expired + timedelta(hours=48))

    def activate_user(self):
        self.is_active = True
        self.activate_key = None
        self.activate_key_expired = None
        self.save()


class ShopUserProfile(models.Model):
    MALE = 'М'
    FEMALE = 'W'
    OTHER = 'O'

    GENDERS = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
        (OTHER, 'И'),
    )

    user = models.OneToOneField(ShopUser, null=False, unique=True, on_delete=models.CASCADE, db_index=True)
    tagline = models.CharField(max_length=128, verbose_name='Тэги', blank=True)
    about_me = models.TextField(verbose_name='Обо мне')
    gender = models.CharField(choices=GENDERS, default=OTHER, verbose_name='Пол', max_length=1)

