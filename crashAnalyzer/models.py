from django.db import models
from django.urls import reverse


# Create your models here.

class CollisionLocation(models.Model):
    collisionId = models.CharField(unique=True, primary_key=True, max_length=250)
    crashDate = models.DateField(auto_now=False, auto_now_add=False)
    crashTime = models.TimeField(auto_now=False, auto_now_add=False)
    borough = models.CharField(max_length=250)
    zipCode = models.CharField(max_length=250)
    lattitude = models.CharField(max_length=250)
    longitude = models.CharField(max_length=250)
    location = models.CharField(max_length=500)
    onStreetName = models.CharField(max_length=250)
    crossStreetName = models.CharField(max_length=250)
    offStreetName = models.CharField(max_length=250)

    def __str__(self):
        """String for representing the Model object."""
        return self.collisionId

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('location-detail', args=[str(self.collisionId)])


class ImpactedPeople(models.Model):
    collisionId = models.ForeignKey(CollisionLocation, blank=False, on_delete=models.CASCADE)
    numPersonsInjured = models.IntegerField()
    numPersonsKilled = models.IntegerField()
    numPedestriansInjured = models.IntegerField()
    numPedestriansKilled = models.IntegerField()
    numCyclistsInjured = models.IntegerField()
    numCyclistsKilled = models.IntegerField()
    numMotoristsInjured = models.IntegerField()
    numMotoristsKilled = models.IntegerField()

    # def __str__(self):
    #     """String for representing the Model object."""
    #     return self.numPersonsInjured

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('people-detail', args=[str(self.collisionId)])


class Vehicle(models.Model):
    collisionId = models.ForeignKey(CollisionLocation, blank=False, on_delete=models.CASCADE)
    contributeVehicle1 = models.CharField(max_length=250)
    contributeVehicle2 = models.CharField(max_length=250)
    contributeVehicle3 = models.CharField(max_length=250)
    contributeVehicle4 = models.CharField(max_length=250)
    contributeVehicle5 = models.CharField(max_length=250)
    vehicleTypeCode1 = models.CharField(max_length=250)
    vehicleTypeCode2 = models.CharField(max_length=250)
    vehicleTypeCode3 = models.CharField(max_length=250)
    vehicleTypeCode4 = models.CharField(max_length=250)
    vehicleTypeCode5 = models.CharField(max_length=250)

    # def __str__(self):
    #     """String for representing the Model object."""
    #     return self.contributeVehicle1

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('vehicle-detail', args=[str(self.collisionId)])


class BikeStation(models.Model):
    StationName = models.CharField(max_length=250)
    StationLocationLat = models.CharField(max_length=250)
    StationLocationLon = models.CharField(max_length=250)
    # the following attributes can be added in future if the nearest crash locations are to be stored
    # nearestCrashLocName = models.CharField(max_length=250,default='Location Not Available')
    # nearestCrashDistance = models.FloatField(max_length=250,default=0)


class googleMapApiKey(models.Model):
    gmapApiKey = models.CharField(max_length=500)
