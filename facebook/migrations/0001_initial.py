# Generated by Django 5.1.4 on 2025-04-25 12:20

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('admin', 'Admin'), ('seller', 'Seller'), ('customer', 'Customer')], max_length=10)),
                ('is_verified', models.BooleanField(default=False)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200)),
                ('quantity', models.IntegerField(null=True)),
                ('price', models.IntegerField(null=True)),
                ('total_price', models.FloatField(null=True)),
                ('product_picture', models.CharField(max_length=300, null=True)),
                ('pw', models.CharField(max_length=200, null=True)),
                ('added_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cname', models.CharField(max_length=200, null=True)),
                ('cpic', models.ImageField(null=True, upload_to='static/category/')),
                ('cdate', models.DateField()),
                ('seller', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Myorders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200)),
                ('quantity', models.IntegerField(null=True)),
                ('price', models.IntegerField(null=True)),
                ('total_price', models.FloatField(null=True)),
                ('product_picture', models.CharField(max_length=300, null=True)),
                ('pw', models.CharField(max_length=200, null=True)),
                ('order_date', models.DateField(null=True)),
                ('status', models.CharField(default='Pending', max_length=200, null=True)),
                ('full_name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=50)),
                ('postal_code', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory_name', models.CharField(max_length=100, null=True)),
                ('category_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facebook.category')),
            ],
        ),
        migrations.CreateModel(
            name='Myproduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('veg_name', models.CharField(max_length=200, null=True)),
                ('price', models.IntegerField()),
                ('discount_price', models.IntegerField()),
                ('product_pic', models.ImageField(null=True, upload_to='static/product/')),
                ('total_discount', models.IntegerField()),
                ('product_quantity', models.CharField(max_length=200)),
                ('pdate', models.DateField()),
                ('product_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facebook.category')),
                ('seller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subcategory_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facebook.subcategory')),
            ],
        ),
        migrations.CreateModel(
            name='UserOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
