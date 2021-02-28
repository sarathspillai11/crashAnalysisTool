# Generated by Django 3.1.2 on 2021-02-24 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crashAnalyzer', '0007_delete_bikestations'),
    ]

    operations = [
        migrations.CreateModel(
            name='BikeStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StationName', models.CharField(max_length=250)),
                ('StationLocationLat', models.CharField(max_length=250)),
                ('StationLocationLon', models.CharField(max_length=250)),
            ],
        ),
    ]