#Bibliotheken einbinden
import RPi.GPIO as GPIO
import time
import requests
#import MySQLdb
import json
import pymongo

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

 
#def logToDb(abstand):
#    db = MySQLdb.connect("localhost", "root", "ultraschall", "messung")
#    curs=db.cursor()
# 
#    try:
#     curs.execute ("INSERT INTO fuellstand (datum, uhrzeit, wert) VALUES (CURRENT_DATE(), NOW(), %.1f);" % abstand)
#     db.commit()
#     print("Done")
#    except:
#     print("Error. Rolling back.")
#     db.rollback()
# 
def logToMongoDb(abstand):
    print("log to azure...")
    uri = "mongodb://andi-mongodb:pTJPyAHcFQU5FQkACPqq3twXHh9PRzKseZnWce1sogpf91ZldTkEJYztbrIEcf2f4eTBWw0QU8rDYsbZo7sU2g==@andi-mongodb.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
    myclient = pymongo.MongoClient(uri)
    mydb = myclient["ultraschall"]
    mycol = mydb["messung"]
    mydict = { "timestamp": time.strftime("%d.%m.%Y %H:%M:%S"), "value": abstand }
    x = mycol.insert_one(mydict)
    
def distanz():
    GPIO.setwarnings(False)
    # setze Trigger auf HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # setze Trigger nach 0.01ms aus LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartZeit = time.time()
    StopZeit = time.time()
 
    # speichere Startzeit
    while GPIO.input(GPIO_ECHO) == 0:
        StartZeit = time.time()
 
    # speichere Ankunftszeit
    while GPIO.input(GPIO_ECHO) == 1:
        StopZeit = time.time()
 
    # Zeit Differenz zwischen Start und Ankunft
    TimeElapsed = StopZeit - StartZeit
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    distanz = (TimeElapsed * 34300) / 2
    return distanz
 
if __name__ == '__main__':
    try:
		print ("Start...")
		while True:
			abstand = distanz()
			print ("Gemessene Entfernung = %.1f cm" % abstand)
			logToMongoDb(abstand)
            # status = post(abstand)
            # print (status)
            
            #30 Sekunden bis zum naechsten Wert
			time.sleep(30)
 
        # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        GPIO.cleanup()