# Generated by Django 3.0.8 on 2020-07-22 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20200722_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='categories',
            field=models.ManyToManyField(related_name='categories', to='auctions.Category'),
        ),
    ]
