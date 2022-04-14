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
    rem_credit = models.IntegerField(default=3000)

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


class ProductHistory(TemplateModel):
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    time_recorded = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = 'prod_hist'
        verbose_name_plural = 'prod_hists'
        indexes = [models.Index(fields=[
            'item',
        ])]


class Order(TemplateModel):
    user = models.ForeignKey(
        CustomUser,
        related_name='order_user',
        related_query_name='user_query',
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(
        Product,
        related_name='order_item',
        related_query_name='item_query',
        on_delete=models.CASCADE
    )
    machine = models.ForeignKey(
        Machine,
        null=True,
        blank=True,
        related_name='order_machine',
        related_query_name='machine_query',
        on_delete=models.CASCADE
    )
    order_id = models.IntegerField()
    quantity = models.IntegerField()

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        constraints = [
            models.UniqueConstraint(fields=['item', 'user'], name='user_item')
        ]
        indexes = [
            models.Index(fields=[
                'machine',
            ]),
            models.Index(fields=[
                'order_id',
            ])
        ]
