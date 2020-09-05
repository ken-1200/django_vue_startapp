# Generated by Django 3.1 on 2020-09-05 13:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_auto_20200823_1254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='withdrawal_datetime',
        ),
        migrations.AddField(
            model_name='payment',
            name='bought_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
