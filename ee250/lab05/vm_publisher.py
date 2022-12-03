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


def temperature_init(latitude,longitude):
    params = {
        'appid' : OWM_API_KEY,
        'lat': latitude,
        'lon': longitude,
        'units': 'imperial'
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

def on_check(avg_temp, avg_pollution):
    
    
    if int(avg_temp) > 280:
        print("Warning: Exceeding Average Temperature Threshold")
        #send "w" character to rpi
        client.publish("172.20.10.4/warn","temp warning")
        
    elif int(avg_pollution) > 180:
        print("Warning: Exceeding Average Carbon Oxide Threshold")
        # send "a" character to rpi
        client.publish("172.20.10.4/warn", "pollution warning")
        #send "LED_ON"
    

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
    	count = 0
    	total_poll = 0
    	total_temp = 0
    	count += 1
    	print("Carbon Monoxide Average Level:")
    	total_poll += pollution_init(latitude,longitude)
    	print("Average Heat Level:")
    	total_temp += temperature_init(latitude,longitude)
    	on_check((total_temp/count),(total_poll/count))
    	time.sleep(5)
    	if(count == 6):
    		total_poll = 0
	    	total_temp = 0
	    	count = 0
		    

