#Bibliotheken einbinden
import RPi.GPIO as GPIO
import time
import requests
import pika

#GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#GPIO Pins zuweisen
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def post(abstand):
    data_json = {'abstand': abstand}
    payload = {'json_payload': data_json}
    r = requests.put('http://192.168.2.105:9090/ultra/ultra', auth=('a', 'a'), data=payload, headers = {'Content-type': 'application/json'})
    #r = requests.post('http://192.168.2.105:9090/ultra/ultra', auth=('a', 'a'), data={'abstand': '124'}, headers = {'Content-type': 'application/json'})

    return r.status_code

def queue(abstand):
    print ("queue...")
    credentials = pika.PlainCredentials('writer', 'writer')
    payload = "timestamp: " + str(time.strftime("%d.%m.%Y %H:%M:%S")) + ", value: "+ str(abstand)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='data')
    print ('publish: ' + payload)
    if abstand > 100:
     channel.basic_publish(exchange='inbound',
                      routing_key='difference',
                      body=payload)
     print(" [x] Sent routing_key 'difference' to exchange 'inbound")
    else:
     channel.basic_publish(exchange='inbound',
                      routing_key='wrong_value',
                      body=payload)
     print(" [x] Sent routing_key 'wrong_value' to exchange 'inbound")
    print ("queue.")
    connection.close()
    print ("queue.")

def distanz():
    print ("distanz...")
    
    print ("GPIO.setwarnings...")
    GPIO.setwarnings(False)
    # setze Trigger auf HIGH
    print ("GPIO.output(GPIO_TRIGGER, True)...")
    GPIO.output(GPIO_TRIGGER, True)
 
    # setze Trigger nach 0.01ms aus LOW
    time.sleep(0.00001)
    
    print ("GPIO.output(GPIO_TRIGGER, False)...")
    GPIO.output(GPIO_TRIGGER, False)
 
    StartZeit = time.time()
    StopZeit = time.time()
 
    # speichere Startzeit
    print ("GPIO.input(GPIO_ECHO) == 0:...")
    while GPIO.input(GPIO_ECHO) == 0:
        StartZeit = time.time()
 
    # speichere Ankunftszeit
    print ("GPIO.input(GPIO_ECHO) == 1:")
    while GPIO.input(GPIO_ECHO) == 1:
        StopZeit = time.time()
 
    # Zeit Differenz zwischen Start und Ankunft
    print ("TimeElapsed = StopZeit - StartZeit...")
    TimeElapsed = StopZeit - StartZeit
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    print ("distanz = (TimeElapsed * 34300) / 2...")
    distanz = (TimeElapsed * 34300) / 2
    print ("distanz.")
    return distanz
 
if __name__ == '__main__':
    try:
        while True:
            for x in range(5):
              abstand = distanz()
              print (x)
              print ("Gemessene Entfernung = %.1f cm" % abstand)
              # status = post(abstand)
              # print (status)
              queue (abstand)
           #60 Sekunden bis zu naechsten 5 Werten
           time.sleep(60)
        # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        GPIO.cleanup()