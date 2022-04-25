from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager

import uuid
import os

PRODUCT_IMAGE_PATH = 'products/'


class TemplateModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, blank=True)

    class Meta:
        abstract = True


def upload_image(instance, filename):
    file_ext = os.path.splitext(filename)[1]
    return '%s/%s/%s' % (PRODUCT_IMAGE_PATH, instance.uuid, file_ext)


class Machine(TemplateModel):
    name = models.TextField(unique=True)

    class Meta:
        verbose_name = 'machine'
        verbose_name_plural = 'machines'


class Product(TemplateModel):
    name = models.TextField()
    desc = models.TextField()
    unit = models.TextField()
    image = models.ImageField(upload_to=upload_image, null=True, blank=True)
    price = models.IntegerField()

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return f'{self.name}'


class CustomUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, blank=True)
    username = None
    email = models.EmailField(unique=True)
    phone = models.TextField(unique=True)
    credit = models.IntegerField(default=3000)

    date_joined = models.DateTimeField(
        'date joined', auto_now_add=True, editable=False
    )
    date_updated = models.DateTimeField(
        'date updated', auto_now=True
    )  # Auto update for every save()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Order(TemplateModel):
    name = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    machine = models.ForeignKey(
        Machine, null=True, blank=True, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        # indexes = [
        #     models.Index(fields=[
        #         'machine',
        #     ]),
        # ]


class OrderItem(TemplateModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = 'order item'
        verbose_name_plural = 'order items'
        constraints = [
            models.UniqueConstraint(
                fields=['item', 'order'], name='order_item'
            )
        ]


class ItemHistory(TemplateModel):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'item history'
        verbose_name_plural = 'item histories'
        indexes = [
            models.Index(fields=[
                'user',
            ]),
        ]
