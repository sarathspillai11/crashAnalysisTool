# Generated by Django 3.1.2 on 2021-02-24 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crashAnalyzer', '0008_bikestation'),
    ]

    operations = [
        migrations.CreateModel(
            name='googleMapApiKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gmapApiKey', models.CharField(max_length=500)),
            ],
        ),
    ]
