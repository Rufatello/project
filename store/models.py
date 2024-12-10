from PIL import Image
from django.db import models
import os
from django.utils.text import slugify
from unidecode import unidecode

from users.models import User

NULLABLE = {
    'blank': True,
    'null': True
}


def generate_slug(instance):
    return slugify(unidecode(instance.name))


def photo_category(instance, file_name):
    return os.path.join('category', instance.slug, file_name)


def photo_subcategory(instance, file_name):
    return os.path.join('subcategory', instance.slug, file_name)


def photo_product(instance, file_name):
    return os.path.join('product', instance.slug, file_name)


class Category(models.Model):
    name = models.CharField(max_length=70, verbose_name='Наименование', **NULLABLE)
    photo = models.ImageField(upload_to=photo_category, verbose_name='Фото', **NULLABLE)
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(unique=True, **NULLABLE)

    def __str__(self):
        return f'{self.name}, {self.slug}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SubCategory(models.Model):
    category = models.ForeignKey(Category, models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=70, verbose_name='Наименование', **NULLABLE)
    photo = models.ImageField(upload_to=photo_subcategory, verbose_name='Фото', **NULLABLE)
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(unique=True, **NULLABLE)

    def __str__(self):
        return f'{self.name}, {self.slug}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=70, verbose_name='Наименование', **NULLABLE)
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(unique=True, **NULLABLE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Цена')
    photo = models.ImageField(upload_to=photo_product, verbose_name='Фото_продукта')

    def __str__(self):
        return f'{self.name}, {self.slug}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self)
        super().save(*args, **kwargs)
        if self.photo:
            self.photo_size()

    def photo_size(self):
        img = Image.open(self.photo.path)
        sizes = [(300, 300, 'small'), (600, 600, 'medium')]
        for width, height, suffix in sizes:
            img_copy = img.copy()
            img_copy.thumbnail((width, height))
            base_path, ext = os.path.splitext(self.photo.path)
            resized_path = f"{base_path}_{suffix}{ext}"
            img_copy.save(resized_path)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='basket')


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Общая стоимость')

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.product.price
        super().save(*args, **kwargs)


