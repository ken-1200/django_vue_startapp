# Generated by Django 3.1 on 2020-09-06 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20200905_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='withdrawal_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
