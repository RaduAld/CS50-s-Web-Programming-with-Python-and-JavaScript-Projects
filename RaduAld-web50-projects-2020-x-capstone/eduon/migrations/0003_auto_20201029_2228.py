# Generated by Django 3.0.8 on 2020-10-29 20:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eduon', '0002_auto_20201029_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='child',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='schclass',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schoclass', to='eduon.Class_school'),
        ),
    ]
