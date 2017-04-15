import paho.mqtt.client as mqtt
import logging
import json
import csv
import os
from geopy.distance import great_circle
from geopy.geocoders import Nominatim

class Location:
    def istScammoKlug(self):
        return False;

    def __init__(self):
        self.userTopics = []

    def callbackGetPos(self, callback):
        self.callback = callback

    def readConfigFromCSV(self, path):
        logging.debug("Read Config")
        if os.path.isfile(path) == False:
             logging.error("Config file >"+path+"< not Found!")
             raise ValueError('Config File >'+path+'< not Found!')
        configObject = [{}, {}, {}]
        with open(path, 'r', encoding='utf8') as csvfile:
            #print("of");
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            #print(spamreader)
            for row in spamreader:
                if(row[0]=="name"):
                    continue
                logging.debug("Read Location "+row[0])
                configObject[0][row[0]] = {"lat": row[1], "lon": row[2], "radius": row[3]}
                configObject[1][row[0]] = {"lat": row[4], "lon": row[5], "radius": row[6]}
                configObject[2][row[0]] = {"lat": row[7], "lon": row[8], "radius": row[9]}
        logging.debug("Config Object: "+str(configObject))
        self.configObject = configObject

    def userToTopic(self, userid, topic, hometown):
        logging.debug("Add User "+str(userid)+" with the Topic "+topic)
        self.userTopics.append({"userid": userid, "topic": topic, "hometown": hometown});



    def on_connect(self, client, userdata, flags, rc):
        logging.debug("Connection establed subscripe to the topics")
        for user in self.userTopics:
            client.subscribe(user["topic"], qos=0)
            logging.debug("Subscribe: "+user["topic"])

    def on_message(self, client, userdata, msg):
        logging.debug("Get a Message")
        userid = None;
        hometown = None;
        for user in self.userTopics:
            if user["topic"] == msg.topic:
                userid = user["userid"]
                hometown = user["hometown"]

        logging.debug("Get Data for User "+str(userid)+" ("+msg.topic+")");


        data = json.loads(msg.payload)


        retData = {"pos": "unknown", "exData": "nope", "userid": userid}
        for key in self.configObject[userid]:
            pos1 = (self.configObject[userid][key]["lat"], self.configObject[userid][key]["lon"])
            pos2 = (data["lat"], data["lon"])
            distance = great_circle(pos1, pos2)
            logging.debug("Distance to "+key+" is "+str(distance.meters));
            maxDistance = int(self.configObject[userid][key]["radius"])+int(data["acc"]);
            if(maxDistance > int(distance.meters)):
                logging.info("Fount User "+str(userid)+" ("+msg.topic+") at "+key)
                retData["pos"] = key
        if(retData["pos"]=="unknown"):
            geolocator = Nominatim()
            location = geolocator.reverse(str(data["lat"])+", "+str(data["lon"]))
            if "town" in location.raw["address"]:
                retData["exData"] = location.raw["address"]["town"];
            elif "county" in location.raw["address"]:
                retData["exData"] = location.raw["address"]["county"];
            elif "state" in location.raw["address"]:
                retData["exData"] = location.raw["address"]["state"];
            elif "country" in location.raw["address"]:
                retData["exData"] = location.raw["address"]["country"];
            else:
                retData["exData"] = "unknown"
                logging.warning("Cant get Data of GeoData :(")
            if(retData["exData"] == hometown):
                resData["pos"] = "hometown"
        logging.debug("Return: "+str(retData));
        self.callback(retData)


    def connection(self, username, password, server):
        logging.debug("Connecting");
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.username_pw_set(username, password=password)
        client.connect(server, 1883, 60)
        logging.debug("Connecting ...");
        self.client = client

    def loop_forever(self):
        self.client.loop_forever()
