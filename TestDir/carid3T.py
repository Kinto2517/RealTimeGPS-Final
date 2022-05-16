import csv
import json
import sys, getopt, pprint
import time
import uuid

import numpy as np
import pandas as pd
import pymongo
import requests
from pymongo import MongoClient
from flaskmongo.models import LoginTime
from datetime import datetime, timedelta
from pykafka import KafkaClient

#########MONGODB BAGLANTI
cluster = "mongodb+srv://admin:admin@cluster1.jxkbw.mongodb.net/carsGeo?retryWrites=true&w=majority"
client = MongoClient(cluster)
db = client['carsGeo']
firstDay1 = db.get_collection('dayLong')

##############JSON URET
lat_3 = []
long_3 = []
carid_3 = []
time_3 = []
a = 0
# start = datetime.now()
# end = start - timedelta(seconds=1800)
# , 'Time': {'$lt': str(start.time()), '$gte': str(end.time())}
for x in firstDay1.find().sort("Time", 1):
    lat_3.append(x['Latitude'])
    long_3.append(x['Longtitude'])
    carid_3.append(x['Carid'])
    time_3.append(x['Time'])
    a += 1



##############DATABASAEDEN ÇEKİLEN BİLGİLERİ DATAFRAMEYE AT
df1 = pd.DataFrame(np.column_stack([lat_3, long_3, carid_3, time_3]),
                   columns=['Latitude', 'Longtitude', 'Carid', 'Time'])
result = df1.to_json('./car_five.json', orient="records")

#
########KAFKA PRODUCER
kclient = KafkaClient(hosts="localhost:9092")
topic = kclient.topics["bbbb"]
producer = topic.get_sync_producer()


################ PRODUCER İÇİN DATA ÜRET
def generate_uuid():
    return uuid.uuid4()

##########KAFKA PRODUCER İLE GEREKLİ BİLGİLERİ JAVASCRİPTE FLASK ÜZERİNDEN GÖNDERİYOR
data = {}
data['a'] = '00001'
def generate_checkpoint(lat_3, long_3, time_3, carid_3):
    b = 0
    for b in range(len(lat_3)):
        data['key'] = data['a'] + "_" + str(generate_uuid())
        data['timestamp'] = time_3[b]
        data['latitude'] = lat_3[b]
        data['longtitude'] = long_3[b]
        data['carid'] = carid_3[b]
        message = json.dumps(data)
        print(message)
        print(carid_3)
        producer.produce(message.encode('ascii'))
        if b == len(lat_3) - 1:
            b = 0
        else:
            b += 1


generate_checkpoint(lat_3, long_3, time_3, carid_3)








# ########### JSON DOSYASINDAN BİLGİ ÇEK
#
# input_file = open("./car_five.json")
# json_array = json.load(input_file)
# lat = []
# long = []
# carid = []
# times = []
# for i in range(a):
#     lat.append(json_array[i]['Latitude'])
#     long.append(json_array[i]['Longtitude'])
#     carid.append(json_array[i]['Carid'])
#     times.append(json_array[i]['Time'])
#
#     print(times)
# GEOJSON KORDİNAT


###########33Sistem saatinden 30dk öncesi
# start = datetime.now()
# end = start - timedelta(seconds=1800)
#
# for x in firstDay1.find( {'Date': 1, 'Time': {'$lt': start, '$gte': end}}):
#     print(x)

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
