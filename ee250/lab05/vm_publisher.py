from tempfile import tempdir
import requests
import json
import time
import paho.mqtt.client as mqtt
import time
import random


OWM_API_KEY = '685108a6134e1bd2927d6037360b88ea'  # OpenWeatherMap API Key 

def pollution_init(latitude,longitude):
    params = {
        'appid' : OWM_API_KEY,
        'lat': latitude,
        'lon': longitude,
    }


    response = requests.get('http://api.openweathermap.org/data/2.5/air_pollution',params)
    if response.status_code == 200:
        data = response.json()
        dumpedData = json.dumps(data)
        loadedData = json.loads(dumpedData)
        carbonOxide = loadedData['list'][0]['components']['co']
        print(carbonOxide)
        return carbonOxide

    else:
         print('error: got response code %d' % response.status_code)
         print(response.text)
         return 0

def radiation_init(latitude,longitude):
    params = {
        'appid' : '615584b858ab9897c727733fb66799d4',
        'lat': latitude,
        'lon': longitude,
    }


    response = requests.get('http://api.openweathermap.org/data/2.5/solar_radiation',params)
    if response.status_code == 200:
        data = response.json()
        dumpedData = json.dumps(data)
        loadedData = json.loads(dumpedData)
        DNI = loadedData['list'][0]['radition']['dni_cs']
        print(DNI)
        return DNI

    else:
         print('error: got response code %d' % response.status_code)
         print(response.text)
         return 0

def temperature_init(latitude,longitude):
    params = {
        'appid' : OWM_API_KEY,
        'lat': latitude,
        'lon': longitude,
    }


    response = requests.get('https://api.openweathermap.org/data/2.5/weather',params)
    if response.status_code == 200:
        data = response.json()
        dumpedData = json.dumps(data)
        loadedData = json.loads(dumpedData)
        temperature = loadedData['main']['temp']
        print(temperature)
        return temperature

    else:
         print('error: got response code %d' % response.status_code)
         print(response.text)
         return 0



      

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def on_check(temp, pollution, radiation):
    
    
    if temp > 282:
        print("Warning: Exceeding Temperature Threshold")
        #send "w" character to rpi
        client.publish("172.20.10.4/warn","temp warning")
        
    elif pollution > 205:
        print("Warning: Exceeding Carbon Oxide Threshold")
        # send "a" character to rpi
        client.publish("172.20.10.4/warn", "pollution warning")
        #send "LED_ON"
    elif radiation > 880:
        print("Warning: Exceeding Radiation Threshold")
        # send "s" character to rpi
        client.publish("172.20.10.4/warn", "rad warning") 
    

if __name__ == '__main__':

    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        latitude = random.randint(-90,90)
        longitude = random.randint(-180,180) 
        print("Carbon Monoxide Level:")
        pollution_init(latitude,longitude)
       	#print("Solar Radiation Level:")
       # radiation_init(latitude,longitude)
        print("Heat Level:")
        temperature_init(latitude,longitude)
        time.sleep(15)
            

