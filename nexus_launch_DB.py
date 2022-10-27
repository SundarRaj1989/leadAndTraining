from pymongo import MongoClient
import certifi
import datetime
import sys

from bson.objectid import ObjectId

from configparser import ConfigParser
import configparser

from flask import session

config = configparser.ConfigParser()
config.read('config.ini')


global con_meetings
global db_meetings
global col_meetings

def connect_registration_db():
  global con_meetings
  global db_meetings
  global col_meetings
  
  ca = certifi.where()
  con_meetings = MongoClient('mongodb+srv://'+
                        config['database']['USERNAME']+':'+
                        config['database']['PASSWORD']+'@'+
                        config['database']['HOST']+'/' +
                        '?retryWrites=true&w=majority', tlsCAFile = ca)
  
  db_meetings = con_meetings.Nexus_launch_DB
  col_meetings = db_meetings.meetings_data


 

def get_registration_meeting_data():
  global col_meetings
  connect_registration_db()
  regd_data = col_meetings.find({}, {"_id":0})
  return regd_data
