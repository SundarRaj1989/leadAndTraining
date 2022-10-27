from pymongo import MongoClient
from flask import Flask, request
from bson.objectid import ObjectId
import certifi

from datetime import datetime
from dateutil.relativedelta import relativedelta

global con
global db
global col_vipList
global col_referal_list

def connect_db():
    global con
    global db
    global col_vipList
    global col_referal_list
    global col_products
    global col_trainer
    global col_inQueComm
    global col_onboard

    ca = certifi.where()

    con = MongoClient('mongodb+srv://Sourav:l9EG8ULwylphgjHS@nexusfieldservice.axvp7.mongodb.net/Lead_Training_Database?retryWrites=true&w=majority')
    db = con.Lead_Training_Database
    col_vipList = db.vipList
    col_referal_list = db.referralList
    col_products = db.productList
    col_trainer = db.trainers
    col_inQueComm = db.inQueCommunication
    col_onboard = db.onboard_details

# =====================================================================================


def insert_product(prod_dict):
    global col_products
    connect_db()

    col_products.insert_one(prod_dict)
    return "saved successfully"

# def get_product_info():
#     global col_prods
#     connect_db()

#     prod = col_prods.find({}, {'_id':0, 'Product_Creation_Date':0})
#     return prod

def get_all_products():
    global col_products
    connect_db()

    all_prods = col_products.find({}, {'_id':0})
    return all_prods

def get_vipUsers_count():
    global col_vipList
    connect_db()

    vip_count = col_vipList.find()
    onboarded_count = col_vipList.find({'payment_clearance':True})
    return [vip_count, onboarded_count]

def get_all_VIP():
    global col_vipList
    connect_db()

    vip_user = col_vipList.find({}).sort('_id',-1).limit(5)
    return vip_user

def get_vipList():
    global col_vipList
    connect_db()

    vip_list = col_vipList.find({}, {'_id':0})
    return vip_list

def get_approved_vipList_comp_id(preorder_id):
    global col_vipList
    connect_db()

    vipList = col_vipList.find({'preOrder_id': preorder_id}, {'_id':0})
    return vipList


def save_onboarding_info(onboarding_info):
    global col_onboard
    connect_db()

    col_onboard.insert_one(onboarding_info)
    return

def get_onboarded_client():
    global col_onboard
    connect_db()

    onboarded_list = col_onboard.find({}, {'_id':0})
    return onboarded_list

def get_approved_vipList():
    global col_vipList
    connect_db()

    vip_list = col_vipList.find({'lead_status':'approved'}, {'_id':0})
    return vip_list

def update_preorder_status(po_id, status, a_date):
    global col_vipList
    connect_db()
    next_month = ''

    if status == 'approved':
        next_mnth = datetime.today() + relativedelta(months=+2)
        next_month = next_mnth.strftime("%B")
        print('next month = ', next_month)
        pc = True
    else:
        next_month = ''
        pc = False

    print('next month = ', next_month)

    col_vipList.update_one(
        {'preOrder_id':po_id}, 
        {'$set':
            {
               'lead_status': status,
               'payment_confirmation_date':  a_date,
               'payment_clearance': pc,
               'estimated_delivery_month' :next_month
            }
        }
    )
    return

def get_unpaid_userInfo(po_id):
    global col_vipList
    connect_db()

    one_user_info = col_vipList.find_one({'email_id':po_id}, {'_id':0})
    return one_user_info

def insert_trainer(trainer_info):
    global col_trainer
    connect_db()

    col_trainer.insert_one(trainer_info)
    return "Saved Successfully"

def get_trainers():
    global col_trainer
    connect_db()

    trainers = col_trainer.find({}, {'_id':0})
    return trainers

def get_trainer_info(trainer_id):
    global col_trainer
    connect_db()

    trainer_data = col_trainer.find({'trainer_id':trainer_id}, {'_id':0 })
    return trainer_data

def save_comm_details(mail_data):
    global col_inQueComm
    connect_db()

    col_inQueComm.insert_one(mail_data)
    return 'insert successfully'

def get_inQue_comm_data():
    global col_inQueComm
    connect_db()

    return col_inQueComm.find({}, {'_id':0})

def update_vipList(vip_list_update):
    global col_vipList
    connect_db()

    col_vipList.update_many(
        {'preOrder_id':vip_list_update['preOrder_id']},
        {'$set': 
            {
            'onboarded' : vip_list_update['onboarded'],
            'onboard_date' : vip_list_update['onboard_date'],
            'onboard_time' : vip_list_update['onboard_time'],
            # 'onboard_scheduled':vip_list_update['onboard_scheduled'],
            'trainer_assigned':vip_list_update['trainer_assigned'],
            'trainer_id': vip_list_update['trainer_id'],
            'trainer_name':vip_list_update['trainer_name'],
            'designation':vip_list_update['designation'],
            'trainer_assigned_date':vip_list_update['trainer_assigned_date']
            }
        },
        upsert=True
    )
    return

def update_slot(slot_allocation_data):
    global col_vipList
    connect_db()

    col_vipList.update_many(
        {'preOrder_id':slot_allocation_data['preOrder_id']},
        {'$set': 
            {'training_slot_status':slot_allocation_data['training_slot_status'], 
            'training_slot_assigned_date':slot_allocation_data['training_slot_assigned_date'],
            'training_slot_assigned':slot_allocation_data['training_slot_assigned'],
            'training_start_date_time':slot_allocation_data['training_start_date_time'],
            'training_end_date_time':slot_allocation_data['training_end_date_time']
            }
        },
        upsert = True
    )
    return

# def get_trainer_info(trainer_id):
#     global col_trainer
#     connect_db()

#     col_trainer.find

# =========================================================
# ======================================
def addFields():
    global col_vipList
    connect_db()

    col_vipList.update_many(
        {}, {'$set': {'onboarded':False}},
        upsert=True
    )
    return
# ==============================================    
# ===============================================================================