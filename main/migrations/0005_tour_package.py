# Generated by Django 5.1 on 2024-08-12 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_travelguide_img_caption'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tour_Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_name', models.CharField(max_length=120)),
                ('country', models.CharField(max_length=50)),
                ('duration', models.IntegerField()),
                ('rating', models.FloatField()),
                ('places_to_visit', models.JSONField()),
                ('hotels', models.JSONField()),
                ('restaurants', models.JSONField()),
                ('activities', models.JSONField()),
                ('tips', models.JSONField()),
                ('timeline', models.JSONField()),
                ('emergency_contacts', models.JSONField()),
            ],
        ),
    ]