# Generated by Django 4.0.3 on 2022-04-23 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainframe', '0003_order_is_paid_alter_order_item_alter_order_machine_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='rem_credit',
            new_name='credit',
        ),
    ]
