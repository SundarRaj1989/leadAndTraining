from flask import request,session
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import re

from configparser import ConfigParser
import configparser

import sensitive_Info_db

config = ConfigParser()
config.read('config.ini', encoding='UTF8')

# *************************Mail config**************************************

def mail_config():
    global mail_server
    data = []
    api_key = ''
    mail_server = ''
    mail_data = sensitive_Info_db.get_sms_details()
    for m in mail_data:
        data.append(m)
    api_key = data[1]['api_key']
    mail_server = data[1]['mail_server']
    return [api_key, mail_server]


# ************************************************************************

def send_to_mail(mailing_Info):
    mail_info = mail_config()
    message = Mail(
        from_email=config['Sendgrid']['FROM_MAIL'],
        to_emails=mailing_Info['mail_id'],
        subject=mailing_Info['subject'],
        html_content=mailing_Info['message'])
    try:
        sg = SendGridAPIClient(mail_info[0])
        response = sg.send(message)
    except Exception as e:
        print(str(e))
    else:
        print(response.status_code)
    return

#=====================================================================================================


 
def send_referral_mail(consumer_email,communication_Info):
    mail_info = mail_config()
    message = Mail(
        from_email=config['Sendgrid']['FROM_MAIL'],
        to_emails=consumer_email,
        subject=communication_Info['sub'],
        html_content=communication_Info['msg'])
    try:
        sg = SendGridAPIClient(mail_info[0])
        response = sg.send(message)
    except Exception as e:
        print(str(e))
    else:
        print(response.status_code)
    return
 
 
def alert_trainer(vip_list_update, ob):
    mail_info = mail_config()
    message = Mail(
        from_email=config['Sendgrid']['FROM_MAIL'],
        to_emails = vip_list_update['trainer_mail_id'],
        subject = 'trainer allocation',
        html_content = 'Hii ' + vip_list_update['trainer_name'] +
                     '<br>You are assigned to "'+ob['company']+'" as a trainer <br>Thank you'
    )
    try:
        sg = SendGridAPIClient(mail_info[0])
        response = sg.send(message)
    except Exception as e:
        print(str(e))
    else:
        print(response.status_code)
    return