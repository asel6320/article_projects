from django.db import models

from django.contrib.auth import get_user_model



class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE, verbose_name='User')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Date of birth')
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars', verbose_name='Avatar')

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

