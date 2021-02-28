from django.shortcuts import render, get_object_or_404, redirect
import pandas as pd
import os
from pathlib import Path
from django.views.generic import (View)
from .models import CollisionLocation, ImpactedPeople, Vehicle, BikeStation
from time import strftime, strptime
import numpy as np
import folium
from math import radians, cos, sin, asin,floor
from sodapy import Socrata


# Create your views here.

class deleteCollisionData(View):
    def get(self, request, *args, **kwargs):

        """This view is used to delete all the data from the CollisionData model"""
        print("in delete collision data #############")
        CollisionLocation.objects.all().delete()
        ImpactedPeople.objects.all().delete()
        Vehicle.objects.all().delete()
        print(" Collision data deleted !!! ")
        return render(request, "index.html")
class homePageView(View):
    def get(self, request, *args, **kwargs):

        """This view is used to load the homepage of the website.
        The values to the drop down available on this page will be
         populated if the data is already available in the database.
         Otherwise default value is placed."""
        print("in home page view ########################")
        crashData = pd.DataFrame(list(CollisionLocation.objects.values()))
        print(crashData.columns)
        try:
            boroughList = set([i for i in set(list(crashData['borough'])) if (i != '')])
            print(boroughList)
        except Exception as e:
            boroughList = {'None'}

        return render(request, "index.html", {"borough": boroughList})


class loadCollisionData(View):
    def get(self, request, *args, **kwargs):
        """This view is used to load the data from the collision dataset.
        For the ease of testing, only a few rows of data are considered for
         time being. This function will load the data from the csv files and store
         it in the database in 3 different tables. Please check the models named
         CollisionLocation, ImpactedPeople, Vehicle from the models.py
         for the data model used."""

        baseDir = Path(__file__).resolve().parent.parent
        # commenting out the following block. Instead reading the data from the sodapy api
        # crashDataPath = os.path.join(baseDir, 'static', r'Motor_Vehicle_Collisions_-_Crashes.csv')
        # crashData = pd.read_csv(crashDataPath, nrows=5000, low_memory=False)
        client = Socrata(r"data.cityofnewyork.us", None)
        results = client.get("h9gi-nx95", limit=500)

        crashData = pd.DataFrame.from_records(results)


        crashData = crashData[pd.notnull(crashData['borough'])]
        crashData = crashData.replace(np.nan, '', regex=True)
        crashData['collision_id'] = [str(i) for i in list(crashData['collision_id'])]
        # print(" original data columns : ", list(crashData.columns))
        CollisionLocation.objects.all().delete()
        ImpactedPeople.objects.all().delete()
        Vehicle.objects.all().delete()
        collisionDf = crashData[['collision_id', 'crash_date', 'crash_time', 'borough', 'zip_code', 'latitude',
                                 'longitude', 'location', 'on_street_name', 'cross_street_name',
                                 'off_street_name']].copy()


        # collisionDf['crash_date'] = [strftime('%Y-%m-%d', strptime(i, '%m/%d/%Y')) for i in
        #                              list(collisionDf['crash_date'])]
        collisionDf['crash_date'] = [strftime('%Y-%m-%d', strptime(i, '%Y-%m-%dT%H:%M:%S.%f')) for i in
                                     list(collisionDf['crash_date'])]


        # collisionDf.to_sql(CollisionLocation)

        print(" data shape : ", collisionDf.shape)
        collisionDf.drop(crashData[(collisionDf['collision_id'] == '') | (collisionDf['collision_id'] == 'nan') | (collisionDf['collision_id'] == None)].index, inplace=True)
        coll_row_iter = collisionDf.iterrows()
        collisionObjs = [
            CollisionLocation(collisionId=row['collision_id'], crashDate=row['crash_date'], crashTime=row['crash_time'],
                              borough=row['borough'], zipCode=row['zip_code'], lattitude=row['latitude'],
                              longitude=row['longitude'], location=row['location'], onStreetName=row['on_street_name'],
                              crossStreetName=row['cross_street_name'], offStreetName=row['off_street_name']) for
            index, row in coll_row_iter]
        CollisionLocation.objects.bulk_create(collisionObjs)
        print("collision objects bulk updated !!")
        peopleObjs = []
        peopleDf = crashData[
            ['collision_id', 'number_of_persons_injured', 'number_of_persons_killed', 'number_of_pedestrians_injured',
             'number_of_pedestrians_killed', 'number_of_cyclist_injured', 'number_of_cyclist_killed',
             'number_of_motorist_injured', 'number_of_motorist_killed']].copy()
        people_row_iter = peopleDf.iterrows()
        # crashDataFromObj = pd.DataFrame(list(CollisionLocation.objects.values()))

        for index, row in people_row_iter:
            # try:
            collisionId = CollisionLocation.objects.get(collisionId=str(row['collision_id']))
            # except Exception as e:
            #     print("Exception while finding collision Id")
            #     collisionId = None
            eachPeopleObj = ImpactedPeople(collisionId=collisionId, numPersonsInjured=row['number_of_persons_injured'],
                                           numPersonsKilled=row['number_of_persons_killed'],
                                           numPedestriansInjured=row['number_of_pedestrians_injured'],
                                           numPedestriansKilled=row['number_of_pedestrians_killed'],
                                           numCyclistsInjured=row['number_of_cyclist_injured'],
                                           numCyclistsKilled=row['number_of_cyclist_killed'],
                                           numMotoristsInjured=row['number_of_motorist_injured'],
                                           numMotoristsKilled=row['number_of_motorist_killed'])
            peopleObjs.append(eachPeopleObj)
        ImpactedPeople.objects.bulk_create(peopleObjs)

        vehicleObjs = []
        vehicleDf = crashData[['collision_id', 'contributing_factor_vehicle_1', 'contributing_factor_vehicle_2',
                               'contributing_factor_vehicle_3', 'contributing_factor_vehicle_4',
                               'contributing_factor_vehicle_5',
                               'vehicle_type_code1', 'vehicle_type_code2','vehicle_type_code_3','vehicle_type_code_4',
                               'vehicle_type_code_5']].copy()

        vehicle_row_iter = vehicleDf.iterrows()
        for index, row in vehicle_row_iter:
            try:
                collisionId = CollisionLocation.objects.get(collisionId=str(row['collision_id']))
            except Exception as e:
                #print(str(e))
                collisionId = None


            eachVehicleObj = Vehicle(collisionId=collisionId, contributeVehicle1=row['contributing_factor_vehicle_1'],
                                     contributeVehicle2=row['contributing_factor_vehicle_2'],
                                     contributeVehicle3=row['contributing_factor_vehicle_3'],
                                     contributeVehicle4=row['contributing_factor_vehicle_4'],
                                     contributeVehicle5=row['contributing_factor_vehicle_5'],
                                     vehicleTypeCode1=row['vehicle_type_code1'],
                                     vehicleTypeCode2=row['vehicle_type_code2'],
                                     vehicleTypeCode3=row['vehicle_type_code_3'],
                                     vehicleTypeCode4=row['vehicle_type_code_4'],
                                     vehicleTypeCode5=row['vehicle_type_code_5'])
            vehicleObjs.append(eachVehicleObj)
        Vehicle.objects.bulk_create(vehicleObjs)

        print(" bulk updation performed !!! ")
        return render(request, "index.html")


class filterBoroughView(View):
    def post(self, request, *args, **kwargs):
        """This view is used to load the data / map based on the borough selected
        by the user from the drop down. This value is used to filter out the data from
        the previously loaded models from the loadCollisionData view"""
        borough = request.POST.get('dropboroughName')

        dataButtonName = request.POST.get('showdata')
        mapButtonName = request.POST.get('showmap')
        if (dataButtonName != None):
            buttonName = dataButtonName
        else:
            buttonName = mapButtonName
        #

        baseDir = Path(__file__).resolve().parent.parent
        # crashDataPath = os.path.join(baseDir,'static',r'collision1000.csv')
        # crashData = pd.read_csv(crashDataPath, low_memory=False)
        print("borough selected : ", borough)
        crashData = pd.DataFrame(list(CollisionLocation.objects.filter(borough=borough).values()))
        # print(list(set(crashData['borough'])))
        crashData.drop(crashData[(crashData['lattitude'] == '') | (crashData['longitude'] == '')].index, inplace=True)
        # print("data read complete from the collision location model")
        print(crashData.shape)
        boroughCollisionIds = list(crashData['collisionId'])
        try:
            crashData = crashData[crashData['location'].notna()]
        except Exception as e:
            # print(" Exception found !!!!!!!!!!!!!!!")
            print(str(e))
        # print(" original data columns : ", list(crashData.columns))

        """As per the requirement, we need only the injured / killed cyclist information, 
                    hence ignoring the columns related to motorist"""

        injuredCyclistFields = [field for field in crashData.columns if ("motorist" not in field.lower())]
        # print(" injured cyclist collision columns : ", injuredCyclistFields)
        # print(set(list(crashData['borough'])))
        # print(borough)
        outputDf = crashData.loc[crashData['borough'] == borough, injuredCyclistFields]
        # print("Data volume based on borough : ", borough, " is ", outputDf.shape)
        # print(outputDf.head(5))

        if buttonName == "Show Map":

            peopleData = pd.DataFrame(list(ImpactedPeople.objects.values()))
            print(list(peopleData.columns))
            print("found ids from people Data")
            print(len(list(peopleData['collisionId_id'])))
            print(len(list(crashData['collisionId'])))

            lattitude_list = list(outputDf['lattitude'])
            longitude_list = list(outputDf['longitude'])

            locZip = list(zip(lattitude_list, longitude_list))
            locs = [(lat, lon) for (lat, lon) in locZip if
                    ((str(lat) not in ('nan', '','0.0')) and (str(lon) not in ('nan', '','0.0')))]
            # print(sorted(locs))
            # print(set([(type(lat), type(lon)) for (lat, lon) in locs]))
            locs = [i for i in locs if ((floor(float(i[0])),floor(float(i[1]))) != (0.0,0.0))]

            meanLat = sum([float(lat) for (lat, lon) in locs]) / len([lat for (lat, lon) in locs])
            meanLon = sum([float(lon) for (lat, lon) in locs]) / len([lon for (lat, lon) in locs])
            print(meanLat, meanLon)

            boroughMap = folium.Map(location=[meanLat, meanLon], zoom_start=11)
            # folium.Marker(location=[meanLat, meanLon], popup="Mean Location", tooltip="Mean Location",
            #               icon=folium.Icon(color='green', icon_color='white', icon='exclamation-triangle', angle=0,
            #                                prefix='fa')).add_to(boroughMap)
            for (id, lat, lon, onStreet, crossStreet, offStreet) in zip(outputDf['collisionId'],outputDf['lattitude'], outputDf['longitude'],
                                                                    outputDf['onStreetName'],
                                                                    outputDf['crossStreetName'],
                                                                    outputDf['offStreetName']):
                # Marker() takes location coordinates
                # as a list as an argument
                # print("[ ", onStreet, " ]#####[ ", crossStreet, " ]##########[ ", offStreet, " ]")
                if (str(onStreet) != 'nan'):
                    loc = onStreet
                elif (str(crossStreet) != 'nan'):
                    loc = crossStreet
                elif (str(offStreet) != 'nan'):
                    loc = offStreet
                else:
                    loc = "unknown location"
                # print(" location : ", loc)

                # print("#######################################")
                injuredCyclists=list(peopleData.loc[peopleData['collisionId_id'] == id,'numCyclistsInjured'])[0]
                killedCyclists = list(peopleData.loc[peopleData['collisionId_id'] == id, 'numCyclistsKilled'])[0]

                crashDetails = """Crash Location:{},
                                Injured Cyclists:{},
                                Killed Cyclists:{}""".format(loc, str(injuredCyclists),
                                                                                          str(killedCyclists))

                folium.Marker([lat, lon], popup=crashDetails, tooltip=loc,
                              icon=folium.Icon(color='red', icon_color='white', icon='exclamation-triangle', angle=0,
                                               prefix='fa')).add_to(boroughMap)

            # Save the file created above

            # crashDataPath = os.path.join(baseDir, 'static', r'Motor_Vehicle_Collisions_-_Crashes.csv')
            mapSavePath = os.path.join(baseDir, 'Template', r'boroughMap.html')
            boroughMap.save(mapSavePath)

            return render(request, "boroughMap.html")
        elif (buttonName == "Show Data"):

            dataSavePath = os.path.join(baseDir, 'Template', r'boroughDataDf.html')
            outputDf.to_html(dataSavePath)
            return render(request, "boroughDataDf.html")


class loadBikeStaionData(View):
    def get(self, request, *args, **kwargs):
        """This view is used to load the bike station information to the database.
        Since we are interested in only storing the station locations, the data is being
        split into two halfes. Please check the BikeStation model from models.py for the
        data model used."""
        BikeStation.objects.all().delete()
        # print("existing data cleared..")
        baseDir = Path(__file__).resolve().parent.parent
        bikeStationPath = os.path.join(baseDir, 'static', 'BikeStationData')
        # print("bike station data located..")
        # print(bikeStationPath)
        all_files = os.listdir(bikeStationPath)
        bikeList = []

        for filename in all_files:
            df = pd.read_csv(bikeStationPath + os.sep + filename,nrows=50, low_memory=False)
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            bikeList.append(df)

        bikeStationData = pd.concat(bikeList, axis=0, ignore_index=True)
        print(" Bike station columns : ")
        print(list(bikeStationData.columns))

        bikeStationObjs = []
        for index, row in bikeStationData.iterrows():


            eachStartStationObj = BikeStation(StationName=row['start station name'],
                                              StationLocationLat=row['start station latitude'],
                                              StationLocationLon=row['start station longitude'])
            bikeStationObjs.append(eachStartStationObj)
            eachEndStationObj = BikeStation(StationName=row['end station name'],
                                            StationLocationLat=row['end station latitude'],
                                            StationLocationLon=row['end station longitude'])
            bikeStationObjs.append(eachEndStationObj)
        BikeStation.objects.bulk_create(bikeStationObjs)

        print(" bulk updation performed for bike stations !!! ")
        return render(request, "index.html")


class showBikesAndCrashesView(View):

    def get(self, request, *args, **kwargs):
        """This is the last view from the website used to show the
        relative locations of bike stations and collision locations."""

        def findNearestLocation(lat1, long1, locList):
            """Using the Haversine Equation to find the distance between two geographical locations"""
            distList = []
            lat1,long1 = map(radians, [lat1, long1])
            for (crashSite, lat2, long2) in locList:
                lat2, long2 = map(radians, [lat2, long2])
                dlon = long2 - long1
                dlat = lat2 - lat1
                a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
                c = 2 * asin(np.sqrt(a))
                distance = 6371 * c
                distList.append((crashSite, distance))
            try:
                nearestLoc = (sorted(distList, key=lambda x: x[1]))[0]
            except Exception as e:
                nearestLoc = ('', 0)
            return nearestLoc

        stationData = pd.DataFrame(list(BikeStation.objects.values()))
        print(stationData.shape)

        crashData = pd.DataFrame(list(CollisionLocation.objects.values()))
        if ((stationData.shape)[0] == 0 or (crashData.shape)[1] == 0):
            return render(request, "noDataFound.html")
        crashData.drop(crashData[(crashData['lattitude'] == '') | (crashData['longitude'] == '')].index, inplace=True)

        #fix:
        crashLocnameList = [(next((el for el in i if el != ''), '')).strip() for i in list(
            zip(crashData['onStreetName'], crashData['crossStreetName'], crashData['offStreetName']))]

        crashLatList = [float(i) for i in list(crashData['lattitude'])]
        crashLonList = [float(i) for i in list(crashData['longitude'])]
        locList = list(zip(crashLocnameList,crashLatList,crashLonList))
        del crashData


        locationZip = list(zip(list(stationData['StationLocationLat']),list(stationData['StationLocationLon'])))
        locationZip = [(float(i[0]),float(i[1])) for i in locationZip]




        stationData['nearestCrashSite'] = [(findNearestLocation(float(a), float(b),locList))[0] for a, b in zip(stationData['StationLocationLat'], stationData['StationLocationLon'])]
        stationData['nearestCrashDistance'] = [np.round(float((findNearestLocation(float(a), float(b), locList))[1]),3) for (a, b) in locationZip]


        lattitude_list = list(stationData['StationLocationLat'])
        longitude_list = list(stationData['StationLocationLon'])

        locZip = list(zip(lattitude_list, longitude_list))
        locs = [(lat, lon) for (lat, lon) in locZip if
                ((str(lat) not in ('nan', '','0.0')) and (str(lon) not in ('nan', '','0.0')))]
        locs = [i for i in locs if ((floor(float(i[0])), floor(float(i[1]))) != (0.0, 0.0))]

        meanLat = sum([float(lat) for (lat, lon) in locs]) / len([lat for (lat, lon) in locs])
        meanLon = sum([float(lon) for (lat, lon) in locs]) / len([lon for (lat, lon) in locs])

        station_Crash_Map = folium.Map(location=[meanLat, meanLon], zoom_start=13)
        # folium.LayerControl().add_to(station_Crash_Map)
        # marker_cluster = MarkerCluster().add_to(station_Crash_Map)
        for (lat, lon, stationName,nearestCrashLoc,crashDistance) in zip(stationData['StationLocationLat'], stationData['StationLocationLon'],
                                           stationData['StationName'],stationData['nearestCrashSite'],stationData['nearestCrashDistance']):

            stationDetails = """Station Name:{}
                                Nearest Crash Station:{},
                                Distance to nearest crash:{} Km""".format(stationName,nearestCrashLoc,str(crashDistance))

            folium.Marker([lat, lon], popup=stationDetails, tooltip="Bike Station",
                          icon=folium.Icon(color='darkblue', icon_color='white', icon='motorcycle', angle=0,
                                           prefix='fa')).add_to(station_Crash_Map)


        crashData = pd.DataFrame(list(CollisionLocation.objects.values()))



        crashData.drop(crashData[(crashData['lattitude'] == '') | (crashData['longitude'] == '')].index, inplace=True)


        for (lat, lon, onStreet, crossStreet, offStreet) in zip(crashData['lattitude'], crashData['longitude'],
                                                                crashData['onStreetName'], crashData['crossStreetName'],
                                                                crashData['offStreetName']):


            if (str(onStreet) != 'nan'):
                loc = onStreet
            elif (str(crossStreet) != 'nan'):
                loc = crossStreet
            elif (str(offStreet) != 'nan'):
                loc = offStreet
            else:
                loc = "unknown location"

            folium.Marker([lat, lon], popup=loc, tooltip="Collision Location",
                          icon=folium.Icon(color='red', icon_color='white', icon='exclamation-triangle', angle=0,
                                           prefix='fa')).add_to(station_Crash_Map)
            """The following can be an extra feature to show all the bike stations falling under a certain radius, which will be encircle in the map"""
            #folium.Circle([lat, lon], popup=loc, tooltip="Area within the 0.5km radius to collsion location : "+loc, radius=500, color='red').add_to(station_Crash_Map)


        baseDir = Path(__file__).resolve().parent.parent
        # crashDataPath = os.path.join(baseDir, 'static', r'Motor_Vehicle_Collisions_-_Crashes.csv')
        mapSavePath = os.path.join(baseDir, 'Template', r'stationCrashMap.html')
        station_Crash_Map.save(mapSavePath)

        return render(request, "stationCrashMap.html")


class deleteBikeStationData(View):
    def get(self, request, *args, **kwargs):

        """This view is used to delete all the data from the BikeStation model"""

        BikeStation.objects.all().delete()
        print(" bike station data deleted !!! ")
        return render(request, "index.html")





