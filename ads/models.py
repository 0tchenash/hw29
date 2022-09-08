from django.db import models
from users.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

# Create your models here.

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=10, validators=[MinLengthValidator(5)], unique=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

class Ad(models.Model):

    Id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, validators=[MinLengthValidator(10)])
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    price = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', default=None, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['name']


class Selection(models.Model):
    items = models.ManyToManyField(Ad)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подборка"
        verbose_name_plural = "Подборки"
        ordering = ['name']