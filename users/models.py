from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.core.exceptions import ValidationError

# Create your models here.
class Location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Местоположение"
        verbose_name_plural = "Местоположения"
        ordering = ['name']

def DateValidator(value: date):
    if date.today().year - value.year < 9:
        raise ValidationError(
            'Your age must be over 9 years old.',
            params = {'year': value.year}
        )



class User(AbstractUser):
    MEMBER = 'member'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLE = [(MEMBER, 'Пользователь'), (ADMIN, 'Админ'), (MODERATOR, 'Модератор')]

    age = models.PositiveIntegerField(null=True)
    birth_date = models.DateField(validators=[DateValidator], null=True)
    role = models.CharField(max_length=25, choices=ROLE, default=MEMBER)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['username']