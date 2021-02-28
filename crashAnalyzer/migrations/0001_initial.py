# Generated by Django 3.1.2 on 2021-02-19 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CollisionLocation',
            fields=[
                ('collisionId', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('crashDate', models.DateField()),
                ('crashTime', models.TimeField()),
                ('borough', models.CharField(max_length=250)),
                ('zipCode', models.CharField(max_length=250)),
                ('lattitude', models.IntegerField()),
                ('longitude', models.IntegerField()),
                ('location', models.CharField(max_length=250)),
                ('onStreetName', models.CharField(max_length=250)),
                ('crossStreetName', models.CharField(max_length=250)),
                ('offStreetName', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contributeVehicle1', models.CharField(max_length=250)),
                ('contributeVehicle2', models.CharField(max_length=250)),
                ('contributeVehicle3', models.CharField(max_length=250)),
                ('contributeVehicle4', models.CharField(max_length=250)),
                ('contributeVehicle5', models.CharField(max_length=250)),
                ('vehicleTypeCode1', models.CharField(max_length=250)),
                ('vehicleTypeCode2', models.CharField(max_length=250)),
                ('vehicleTypeCode3', models.CharField(max_length=250)),
                ('vehicleTypeCode4', models.CharField(max_length=250)),
                ('vehicleTypeCode5', models.CharField(max_length=250)),
                ('collisionId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crashAnalyzer.collisionlocation')),
            ],
        ),
        migrations.CreateModel(
            name='ImpactedPeople',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numPersonsInjured', models.IntegerField()),
                ('numPersonsKilled', models.IntegerField()),
                ('numPedestriansInjured', models.IntegerField()),
                ('numPedestriansKilled', models.IntegerField()),
                ('numCyclistsInjured', models.IntegerField()),
                ('numCyclistsKilled', models.IntegerField()),
                ('numMotoristsInjured', models.IntegerField()),
                ('numMotoristsKilled', models.IntegerField()),
                ('collisionId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crashAnalyzer.collisionlocation')),
            ],
        ),
    ]