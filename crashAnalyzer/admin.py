from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models import CollisionLocation, ImpactedPeople, Vehicle, BikeStation, googleMapApiKey


@admin.register(CollisionLocation)
class collisionAdmin(ImportExportModelAdmin):
    list_display = ('collisionId', 'crashDate', 'crashTime', 'borough',
                    'zipCode', 'lattitude', 'longitude', 'location', 'onStreetName',
                    'crossStreetName', 'offStreetName')


@admin.register(ImpactedPeople)
class peopleAdmin(ImportExportModelAdmin):
    list_display = ('collisionId', 'numPersonsInjured', 'numPersonsKilled',
                    'numPedestriansInjured', 'numPedestriansKilled',
                    'numCyclistsInjured', 'numCyclistsKilled', 'numMotoristsInjured',
                    'numMotoristsKilled')


@admin.register(Vehicle)
class vehicleAdmin(ImportExportModelAdmin):
    list_display = ('collisionId', 'contributeVehicle1', 'contributeVehicle2',
                    'contributeVehicle3', 'contributeVehicle4', 'contributeVehicle5',
                    'vehicleTypeCode1', 'vehicleTypeCode2',
                    'vehicleTypeCode3', 'vehicleTypeCode4', 'vehicleTypeCode5')


@admin.register(BikeStation)
class stationAdmin(ImportExportModelAdmin):
    list_display = ('StationName', 'StationLocationLat', 'StationLocationLon')


@admin.register(googleMapApiKey)
class mapAdmin(ImportExportModelAdmin):
    list_display = ('gmapApiKey',)
