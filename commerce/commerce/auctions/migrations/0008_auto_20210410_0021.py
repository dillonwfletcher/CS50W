# Generated by Django 3.1.7 on 2021-04-10 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210410_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='winner',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
