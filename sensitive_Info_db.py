from pymongo import MongoClient
import datetime
import sys
import certifi

from bson.objectid import ObjectId

global con
global db
global col

def connect_db():
  global con
  global db
  global col
  ca = certifi.where()
  con = MongoClient('mongodb+srv://Sourav:l9EG8ULwylphgjHS@nexusfieldservice.axvp7.mongodb.net/Properties?retryWrites=true&w=majority',tlsCAFile = ca)
  db = con.Properties
  col = db.sensitive_access

def get_sms_details():
  global col
  connect_db()
  sensitive_Data = col.find({})
  return sensitive_Data