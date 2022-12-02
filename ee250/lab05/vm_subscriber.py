import paho.mqtt.client as mqtt
import time

# callback for button    
def on_button(client, userdata, message):
    print("on_button: " + message.topic + " " + "\"" + 
        str(message.payload, "utf-8") + "\"")
    print("Button pressed. Warning acknowledged.")

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to the ultrasonic ranger topic here     
    client.subscribe("172.20.10.4/button")
    client.message_callback_add("172.20.10.4/button",on_button)    
    

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)
