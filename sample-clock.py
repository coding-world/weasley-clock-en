from location import Location
from servo import Servo
import logging
import lcd_display
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARNING)
servo = Servo()

lcd_display.lcd_init()

def getData(d):
    numer = "";
    if(d["userid"] == 1):
        number = "2"
    elif(d["userid"] == 2):
        number = "1"
    elif(d["userid"] == 0):
         number = "3"

    if(d["pos"]=="home"):
        number = number + "4"
    elif(d["pos"]=="office"):
        number = number + "3"
    elif(d["pos"]=="hometown"):
        number = number + "2"
    elif(d["pos"]=="unknown"):
        number = number + "1"
        lcd_display.lcd_string(str(d["exData"]), 1)

    servo.writeNumber(int(number))
    print(str(d))

location = Location();
#location.readConfigFromCSV("/home/pi/ssp/config.csv");
location.readConfigFromCSV("/app/config.csv");
location.userToTopic(0, "owntracks/user1/handy", "Flensburg")
location.userToTopic(1, "owntracks/user2/handy", "Berlin")
location.userToTopic(2, "owntracks/user3/handy", "Flensburg")
location.connection("username", "password", "mqtt.example.com");
location.callbackGetPos(getData)
location.loop_forever();
