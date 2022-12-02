import paho.mqtt.client as mqtt
import time
import grovepi
import grove_rgb_lcd as lcd

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest and add callback
    client.subscribe("172.20.10.4/warn")
    client.message_callback_add("172.20.10.4/warn",warn_callback)
   


#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

#button callback
def on_button(client, userdata, msg):
    print("on_button: " + msg.topic + " " + str(msg.payload, "utf-8"))
    

#lcd callback
def warn_callback(client,userdata,msg):
    data = str(msg.payload, "utf-8")
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))
    grovepi.digitalWrite(buzzer, 1)
    if(data == "temp warning"):
      lcd.setText_norefresh("Warning: Over Temperature Threshold    ")
      lcd.setRGB(255, 87, 51)
      
      
    elif(data == "pollution warning"):
      lcd.setText_norefresh("Warning: Over Air Pollution Threshold     ")
      lcd.setRGB(255, 255, 0)
        

    elif(data == "rad warning"):
      lcd.setText_norefresh("Warning: Over Radiation Threshold      ")
      lcd.setRGB(255, 0, 0)


if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    grovepi.set_bus("RPI_1")
    
    # Port variables
    button = 2
    buzzer = 4

    grovepi.pinMode(button,"INPUT")
    grovepi.pinMode(buzzer,"OUTPUT")

    while True:
        # publish message when button is pressed
        if(grovepi.digitalRead(button)== 1):
            client.publish("172.20.10.4/button", "Button pressed!")
            lcd.setText_norefresh("                                    ")
            lcd.setRGB(0, 255, 0)
            grovepi.digitalWrite(buzzer, 0)
            time.sleep(1)
          
        time.sleep(1)

