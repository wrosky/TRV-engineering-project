# Generated by Django 5.0.7 on 2024-10-29 14:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_privatechat_privatemessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('num_days', models.PositiveIntegerField()),
                ('flight_arrival', models.CharField(max_length=100)),
                ('flight_departure', models.CharField(max_length=100)),
                ('flight_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('car_time', models.DurationField()),
                ('car_distance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('car_price_per_person', models.DecimalField(decimal_places=2, max_digits=10)),
                ('accommodation_name', models.CharField(max_length=100)),
                ('accommodation_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transport_name', models.CharField(max_length=100)),
                ('transport_type', models.CharField(max_length=100)),
                ('transport_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('visa_required', models.BooleanField(default=False)),
                ('visa_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('attractions', models.ManyToManyField(blank=True, to='base.attraction')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
