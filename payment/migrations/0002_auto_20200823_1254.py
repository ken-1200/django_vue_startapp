# Generated by Django 3.1 on 2020-08-23 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='user_email',
            field=models.EmailField(max_length=254),
        ),
    ]
