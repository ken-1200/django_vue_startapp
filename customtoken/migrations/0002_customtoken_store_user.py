# Generated by Django 3.1.3 on 2020-11-22 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
        ('customtoken', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customtoken',
            name='store_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.store'),
        ),
    ]
