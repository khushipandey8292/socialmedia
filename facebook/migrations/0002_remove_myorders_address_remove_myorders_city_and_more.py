# Generated by Django 5.1.4 on 2025-04-25 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facebook', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myorders',
            name='address',
        ),
        migrations.RemoveField(
            model_name='myorders',
            name='city',
        ),
        migrations.RemoveField(
            model_name='myorders',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='myorders',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='myorders',
            name='postal_code',
        ),
    ]
