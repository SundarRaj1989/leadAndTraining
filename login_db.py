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


global con_login_dealer
global db_login_dealer
global col_login_dealer
global col_login_consumer




#  login section
def connect_login_db():
    global con_login_dealer
    global db_login_dealer
    global col_login_dealer
    global col_login_consumer

    #auth = config['Authorization']['DB_NAME']
    #auth_col = config['Authorization']['COLLECTION_NAME_RETAILERS']
    ca = certifi.where()
    con_login_dealer = MongoClient('mongodb+srv://'+config['database']['USERNAME']+':'
                                            +config['database']['PASSWORD']+'@'
                                            +config['database']['HOST']+'/'
                                            +config['Authorization']['DB_NAME']
                                            +'?retryWrites=true&w=majority',tlsCAFile = ca)

    # con_login = MongoClient('mongodb+srv://Sourav:l9EG8ULwylphgjHS@nexusfieldservice.axvp7.mongodb.net/Authorization?retryWrites=true&w=majority')
    db_login_dealer = con_login_dealer.Authorization
    col_login_dealer = db_login_dealer.dealer_credentials
    col_login_consumer = db_login_dealer.consumer_creds


def search_authorization_by_id(u_id):
   global col_login_dealer
   connect_login_db()
   searched_data_list = []
   searched_data = col_login_dealer.find({'user_id':str(u_id)},{"_id":0})
   return searched_data

def update_one_password(email, check):
    global col_login_dealer
    connect_login_db()
    col_login_dealer.update_one({"user_id": str(email)}, {'$set' :{'password':check['password']} })
    return

def check_password(email):
    global col_login_dealer
    connect_login_db()
    searched_data = col_login_dealer.find({'user_id':str(email)},{"_id":0})
    return searched_data





#================================================Dealer Account===============================================================================
#=========================================================================================================
global con_dealer_account
global db_dealer_account
global col_dealer_account
global col_employee_info
global col_terms_n_co


def connect_account_db():
    global con_dealer_account
    global db_dealer_account
    global col_dealer_account
    global col_employee_info
    global col_terms_n_co

    ca = certifi.where()
    con_dealer_account = MongoClient('mongodb+srv://'+config['database']['USERNAME']+':'
                                            +config['database']['PASSWORD']+'@'
                                            +config['database']['HOST']+'/'
                                            +config['Dealer_Account']['DB_NAME']
                                            +'?retryWrites=true&w=majority',tlsCAFile = ca)
    db_dealer_account = con_dealer_account.Dealer_account_DB
    col_dealer_account = db_dealer_account.basic_details
    col_employee_info = db_dealer_account.employee_info
    col_terms_n_co = db_dealer_account.text_asset

def get_account_activation_status_details(org_id):
    global col_dealer_account
    connect_account_db()
    dealer_data = col_dealer_account.find( {'$and': [{"dealer_id" : str(org_id) },{"dealer_activation_status" : True} ]},{"_id":0})
    return dealer_data