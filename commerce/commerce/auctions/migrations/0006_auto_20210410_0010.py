# Generated by Django 3.1.7 on 2021-04-10 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20210410_0009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='winner',
            field=models.CharField(default='none', max_length=64),
        ),
    ]
