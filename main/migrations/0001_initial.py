# Generated by Django 5.1 on 2024-08-12 18:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TravelGuide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=50)),
                ('country_name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tourist_Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('travel_guide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.travelguide')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('travel_guide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.travelguide')),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('travel_guide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.travelguide')),
            ],
        ),
        migrations.CreateModel(
            name='Emergency_Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity', models.CharField(max_length=50)),
                ('value', models.TextField()),
                ('travel_guide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.travelguide')),
            ],
        ),
    ]