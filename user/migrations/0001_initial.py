# Generated by Django 3.0.8 on 2020-08-05 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.EmailField(max_length=254, unique=True)),
                ('user_password', models.CharField(max_length=30)),
                ('withdrawal_datetime', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
