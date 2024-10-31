# Generated by Django 5.0.7 on 2024-10-29 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_alter_attraction_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attraction',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='trip',
            name='attractions',
            field=models.ManyToManyField(blank=True, related_name='trips', to='base.attraction'),
        ),
    ]