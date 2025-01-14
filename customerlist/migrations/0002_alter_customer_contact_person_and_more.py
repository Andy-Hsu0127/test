# Generated by Django 4.2.17 on 2025-01-09 02:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customerlist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='contact_person',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='聯絡人'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='contact_phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='電話'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='創建時間'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='創建人'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='unified_number',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='統一編號'),
        ),
    ]
