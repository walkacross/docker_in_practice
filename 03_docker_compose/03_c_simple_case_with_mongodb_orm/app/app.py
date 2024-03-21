#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 20:13:57 2018

@author: allen
"""
import random, os, json, datetime, time

from flask import Flask, Response
from pymongo import MongoClient
from bson import json_util


app = Flask(__name__)

MONGO_URI = "mongodb://mongodb:27017"  # "mongodb:<container_name>:27017"
mongdb_client= MongoClient(MONGO_URI)
random_numbers = mongdb_client.demo.random_numbers

time.sleep(5) # hack for the mongoDb database to get running



######################
##
##########################
from pymodm.connection import connect
from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields

# Connect to MongoDB and call the connection "my-app".
connect("mongodb://mongodb:27017/myDatabase", alias="my-app")
class User(MongoModel):
    email = fields.EmailField(primary_key=True)
    first_name = fields.CharField()
    last_name = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-app'

@app.route("/")
def hello():
    html =  "<h3> Hello world...</h3>"
    #User('user@email.com', name, 'Ross').save()
    return html

@app.route("/add_user/<name>")
def add_user(name):
    #User('user@email.com', name, 'Ross').save()
    html =  "<h3> Hello </h3>"
    User('user@email.com', name, 'Ross').save()
    return "name {} save to database".format(name)



@app.route("/random/<int:lower>/<int:upper>")
def random_generator(lower, upper):
    number = str(random.randint(lower, upper))
    random_numbers.update(
        {"_id" : "lasts"},
        {"$push" : {
            "items" : {
                "$each": [{"value" : number, "date": datetime.datetime.utcnow()}],
                "$sort" : {"date" : -1},
                "$slice" : 5
            }
        }},
        upsert=True
    )

    return Response(number, status=200, mimetype='application/json')


@app.route("/random-list")
def last_number_list():
    last_numbers = list(random_numbers.find({"_id" : "lasts"}))
    extracted = [d['value'] for d in last_numbers[0]['items']]

    return Response(json.dumps(extracted, default=json_util.default), status=200, mimetype='application/json')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=port)
