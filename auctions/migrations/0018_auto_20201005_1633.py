# Generated by Django 3.0.8 on 2020-10-05 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_auto_20201005_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.TextField(blank=True, max_length=250),
        ),
    ]
