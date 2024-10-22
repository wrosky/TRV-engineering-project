# Generated by Django 5.0.7 on 2024-10-15 18:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_friendlist_friendrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendlist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='friend_list', to=settings.AUTH_USER_MODEL),
        ),
    ]