# Generated by Django 5.1.1 on 2024-10-12 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_seller_name_remove_seller_shop_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_seller',
            new_name='seller',
        ),
    ]
