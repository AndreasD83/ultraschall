Alles hier beschrieben!

Installation reqeusts!
sudo apt-get install python-requests


https://tutorials-raspberrypi.de/entfernung-messen-mit-ultraschallsensor-hc-sr04/?subscribe=success#488


r = requests.post('http://192.168.2.105:9090/ultra/ultra', auth=('a', 'a'), verify=False, json={"abstand": "11"}, headers = {'Content-type': 'application/json'})



https://tutorials-raspberrypi.de/lokale-mysql-datenbank-raspberry-pi-datenlogger/




USer zum Zugriff von Desktop:
CREATE USER 'admin'@'%'
  IDENTIFIED BY 'desKt0p'
  
  create database messung;
  
  
  CREATE TABLE fuellstand (
    id int NOT NULL AUTO_INCREMENT,
    datum DATE,
    uhrzeit TIME,
    wert FLOAT,
    PRIMARY KEY(id)
);


GRANT ALL PRIVILEGES ON messung.* TO 'admin'@'*';

GRANT ALL PRIVILEGES ON messung.* TO 'admin'@'*' WITH ADMIN OPTION;





Dienst zum Messen
sudo chmod 644 /lib/systemd/system/ultraschall.service
chmod +x /home/openhabian/fuellstand/ultraschallsensor_entfernung_mongo.py  
sudo systemctl daemon-reload
sudo systemctl enable ultraschall.service
sudo systemctl start ultraschall.service


sudo systemctl status ultraschall.service



PYmongo isntallieren:
https://andyfelong.com/2016/03/using-python-with-mongodb-on-raspberry-pi-2/


