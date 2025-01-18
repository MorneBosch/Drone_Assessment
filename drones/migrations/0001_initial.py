# Generated by Django 5.1.5 on 2025-01-18 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('weight_limit', models.IntegerField()),
                ('battery_capacity', models.IntegerField()),
                ('state', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('weight', models.FloatField()),
                ('code', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='medications/')),
            ],
        ),
    ]
