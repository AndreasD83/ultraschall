#Bibliotheken einbinden
import RPi.GPIO as GPIO
import time
import requests

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
            abstand = distanz()
            print ("Gemessene Entfernung = %.1f cm" % abstand)
            # status = post(abstand)
            # print (status)
            
            #30 Sekunden bis zum naechsten Wert
            time.sleep(30)
 
        # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        GPIO.cleanup()