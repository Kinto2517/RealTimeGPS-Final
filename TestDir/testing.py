import csv
import json
import sys, getopt, pprint
import time
import uuid

import numpy as np
import pandas as pd
import pymongo
import requests
from flask_login import current_user
from pymongo import MongoClient
from flaskmongo.models import LoginTime
from datetime import datetime, timedelta
from pykafka import KafkaClient

#########MONGODB BAGLANTI
cluster = "mongodb+srv://admin:admin@cluster1.jxkbw.mongodb.net/carsGeo?retryWrites=true&w=majority"
client = MongoClient(cluster)
db = client['carsGeo']
firstDay1 = db.get_collection('firstDay1')

##############JSON URET

lat_5 = []
long_5 = []
carid_5 = []
time_5 = []
a = 0
myquery = {"Carid": "5"}
for x in firstDay1.find(myquery).sort("Time", 1):
    lat_5.append(x['Latitude'])
    long_5.append(x['Longtitude'])
    carid_5.append(x['Carid'])
    time_5.append(x['Time'])
    a += 1

##############DATABASAEDEN ÇEKİLEN BİLGİLERİ DATAFRAMEYE AT
df1 = pd.DataFrame(np.column_stack([lat_5, long_5, carid_5, time_5]),
                   columns=['Latitude', 'Longtitude', 'Carid', 'Time'])
result = df1.to_json('./car_five.json', orient="records")

########### JSON DOSYASINDAN BİLGİ ÇEK
start = datetime.now()
end = start - timedelta(seconds=1800)
print(start)
print(end)
for x in firstDay1.find( {'Date': 1, 'Time': {'$lt': start, '$gte': end}}):
    print(x)

input_file = open("./car_five.json")
json_array = json.load(input_file)
lat = []
long = []
carid = []
times = []
for i in range(a):
    lat.append(json_array[i]['Latitude'])
    long.append(json_array[i]['Longtitude'])
    carid.append(json_array[i]['Carid'])
    times.append(json_array[i]['Time'])


#
# ########KAFKA PRODUCER
# kclient = KafkaClient(hosts="localhost:9092")
# topic = kclient.topics["geodata_final"]
# producer = topic.get_sync_producer()
#
#
# #
# # cnt = 0
# # while True:
# #     if cnt==1250:
# #         break
# #     message = ("HelloBitch-"+str(cnt)).encode('ascii')
# #     producer.produce(message)
# #     print(message)
# #     cnt += 1
#
# ################ PRODUCER İÇİN DATA ÜRET
# def generate_uuid():
#     return uuid.uuid4()
#
#
# data = {}
# data['a'] = '00001'
#
# usernamedata = current_user.username
#
# print(usernamedata)
#
# def generate_checkpoint(lat, long, times, carid):
#     b = 0
#     for b in range(len(lat)):
#         data['key'] = data['a'] + "_" + str(generate_uuid())
#         data['timestamp'] = times[b]
#         data['latitude'] = lat[b]
#         data['longtitude'] = long[b]
#         data['carid'] = carid[b]
#         message = json.dumps(data)
#         print(message)
#         producer.produce(message.encode('ascii'))
#         time.sleep(1)
#
#         if b == len(lat) - 1:
#             b = 0
#         else:
#             b += 1
#
#
# generate_checkpoint(lat, long, times, carid)
#
# # GEOJSON KORDİNAT


###########33Sistem saatinden 30dk öncesi

# {"Carid": { $in: [ "3", "5" ] } }

############# Bağlantı yapıldıktan sonra csv dosyasını okuyup değerleri çekiyoruz.
####### Bu değerleri listeye dönüştürüp bu listeyi dataframe olarak okutup bu dataframeyi to_dict ile databaseye atıyoruz.
# cluster = "mongodb+srv://admin:admin@cluster1.jxkbw.mongodb.net/carsGeo?retryWrites=true&w=majority"
# client = MongoClient(cluster)
# db = client['carsGeo']
# firstDay1 = db.get_collection('firstDay1')

######### CSV DOSYASI OKUYARAK BELİRLİ KESMELERDEKİ DATALARI OKUR VE DATABASEYE YÜKLER(İLK 30DK)
# data1 = pd.read_csv('final2.csv', usecols=['date', 'time', 'latitude', 'longtitude', 'carid'])
# birA = data1.values[0:40]
# list1 = birA.tolist()
# df1 = pd.DataFrame(list1, columns=['Date', 'Time', 'Latitude', 'Longtitude', 'Carid']).to_dict(orient='records')
# # result = df.to_json('a.json', orient="records")
# ikiA = data1.values[392:420]
# list2 = ikiA.tolist()
# df2 = pd.DataFrame(list2, columns=['Date', 'Time', 'Latitude', 'Longtitude', 'Carid']).to_dict(orient='records')
#
# ucA = data1.values[555:590]
# list3 = ucA.tolist()
# df3 = pd.DataFrame(list3, columns=['Date', 'Time', 'Latitude', 'Longtitude', 'Carid']).to_dict(orient='records')
#
# dortA = data1.values[1470:1510]
# list4 = dortA.tolist()
# df4 = pd.DataFrame(list4, columns=['Date', 'Time', 'Latitude', 'Longtitude', 'Carid']).to_dict(orient='records')
#
# firstDay1.insert_many(df1)
# firstDay1.insert_many(df2)
# firstDay1.insert_many(df3)
# firstDay1.insert_many(df4)


########## JSON DOSYASINDAN LAT VE LONG ÇEKER
# input_file = open("./a.json")
# json_array = json.load(input_file)
# for i in range(30):
#     lat = json_array[i]['Latitude']
#     long = json_array[i]['Longtitude']
#     carid = json_array[i]['Carid']
#     print(lat, long)


# dateVal = data0['date'].values
# timeVal = data0['time'].values
# latVal = data0['latitude'].values
# longVal = data0['longtitude'].values
# caridVal = data0['carid'].values
# bir_date1 = dateVal[0:270]
# bir_time1 = timeVal[0:270]
# bir_lat1 = latVal[0:270]
# bir_long1 = longVal[0:270]
# bir_carid1 = caridVal[0:270]
# bir_date2 = dateVal[271:391]
# bir_time2 = timeVal[271:391]

# bir_lat2 = latVal[271:391]
# bir_long2 = longVal[271:391]
# bir_carid2 = caridVal[271:391]

# cluster = "mongodb://admin:admin@cluster1-shard-00-00.jxkbw.mongodb.net:27017,cluster1-shard-00-01.jxkbw.mongodb.net:27017,cluster1-shard-00-02.jxkbw.mongodb.net:27017/carsGeo?ssl=true&replicaSet=atlas-n7170e-shard-0&authSource=admin&retryWrites=true&w=majority"
# client = MongoClient(cluster)
# db = client['carsGeo']
# csvfile = open('final2.csv', 'r')
# reader = csv.DictReader(csvfile)
# db.segment.drop()
# firstDay = db.get_collection('firstDay')
# header = ['date', "time", "latitude", "longtitude", "carid"]
#
# a = 0
# for each in reader:
#
#     row = {}
#     for field in header:
#         row[field] = each[field]
#
#     firstDay.insert_one(row)
#     a += 1

# <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAHJRvG5QeD1tHOe3Y2sJU9anE8ll7BN8s" async
#             defer></script>
#     <link
#             rel="stylesheet"
#             href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
#             integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="
#             crossorigin=""
#     />
#     <script
#             src="https://unpkg.com/leaflet@1.7.1/dist/leaflet-src.js"
#             integrity="sha512-I5Hd7FcJ9rZkH7uD01G3AjsuzFy3gqz7HIJvzFZGFt2mrCS4Piw9bYZvCgUE0aiJuiZFYIJIwpbNnDIM6ohTrg=="
#             crossorigin=""
#     ></script>
#     <script src="https://unpkg.com/leaflet.gridlayer.googlemutant@latest/dist/Leaflet.GoogleMutant.js"></script>
