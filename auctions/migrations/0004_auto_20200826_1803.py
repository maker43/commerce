# Generated by Django 3.0.8 on 2020-08-26 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20200826_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='listing',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
