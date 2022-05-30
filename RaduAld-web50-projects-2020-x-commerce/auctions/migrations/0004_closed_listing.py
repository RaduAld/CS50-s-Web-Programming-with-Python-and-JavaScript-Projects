# Generated by Django 3.0.8 on 2020-07-17 14:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_listing_bid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Closed_listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=500)),
                ('image_url', models.CharField(blank=True, max_length=1000000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_creator', to=settings.AUTH_USER_MODEL)),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_winner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]