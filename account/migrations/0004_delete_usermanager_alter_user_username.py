# Generated by Django 4.0.6 on 2022-08-07 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_usermanager'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserManager',
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=255, unique=True, verbose_name='username'),
        ),
    ]
