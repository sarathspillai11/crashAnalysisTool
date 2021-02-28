# Generated by Django 3.1.2 on 2021-02-24 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crashAnalyzer', '0005_auto_20210222_2356'),
    ]

    operations = [
        migrations.CreateModel(
            name='BikeStations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StationName', models.CharField(max_length=250)),
                ('StationLocationLat', models.CharField(max_length=250)),
                ('StationLocationLon', models.CharField(max_length=250)),
            ],
        ),
    ]
