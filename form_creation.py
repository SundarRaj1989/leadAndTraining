from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DecimalField, BooleanField
from wtforms.fields import EmailField, TelField
from wtforms.validators import DataRequired, Email, InputRequired, ValidationError

import configparser

import lead_train_db

config = configparser.ConfigParser()
config.read('config.ini')

class product_form(FlaskForm):
    prod_name = StringField('product_name', validators=[DataRequired()], render_kw={"placeholder": "Product Name"})
    prod_price = DecimalField('product_price', places=2, rounding=None, validators=[], render_kw={"placeholder": "Product Price"})
    prod_create = SubmitField('Create Product')


class trainer_form(FlaskForm):
    provinces_canada_list_of_tuples = []
    provinces_canada_list_of_tuples.append(('' , 'Select Province'))
    
    states_us_list_of_tuples = []
    states_us_list_of_tuples.append(('', 'Select State'))

    prod_list = []
    prod_list.append(('', 'Select Product'))
    p_list = lead_train_db.get_all_products()

    for p in p_list:
        prod_value = p['Product_id'] + '_' + p['Product_Price'] + '_' + p['Product_name']
        prod_tupple = (prod_value, p['Product_name'])
        prod_list.append(prod_tupple)

    trainer_f_name = StringField('Trainer First Name', validators=[DataRequired()], render_kw={"placeholder": "Enter First Name"})
    trainer_l_name = StringField('Trainer Last Name', validators=[DataRequired()], render_kw={"placeholder": "Enter Last Name"})
    designation = StringField('Trainer Designation', validators=[DataRequired()], render_kw={"placeholder": "Enter designation"})
    email_id = EmailField('Email Id', validators=[DataRequired('Please enter your email id'), Email(message='Please enter valid email id')], render_kw={"placeholder": "Email Id"})
    c_num = TelField('Contact Number', validators=[DataRequired()], render_kw={"placeholder": "Contact Number"})
    state = StringField('State', validators=[DataRequired()], render_kw={"placeholder": "State"})
    city = StringField('City', validators=[DataRequired()], render_kw={"placeholder": "City"})    
    nexus_product = SelectField('Select Product', choices=prod_list, validators=[DataRequired()])
    submit = SubmitField(label=('Add Trainer'))

    provinces_canada = config['states']['CANADA'].split(', ')
    for i in provinces_canada:
        single_province_tuple = (i,i)
        provinces_canada_list_of_tuples.append(single_province_tuple)

    ca_States = SelectField('Select Province', choices=provinces_canada_list_of_tuples)

    states_us = config['states']['US'].split(', ')
    for s in states_us:
        single_state_tuple = (s,s)
        states_us_list_of_tuples.append(single_state_tuple)

    us_States = SelectField('Select State', choices=states_us_list_of_tuples)

    emp_fld = SelectField('Select', choices=[('' , 'Select')])

    country_1 = BooleanField('Canada')
    country_2 = BooleanField('US')

# class slot_alotment(FlaskForm):
#     user_list = []
#     user_list.append(('', 'Select a Company'))

#     ob_userList = lead_train_db.get_onboarded_client()
#     for ob in ob_userList:
#         if ob['training_slot_status'] == 'Not provided':
#             users = ob['preOrder_id']+'_'+ob['company']
#             user_list.append(ob['company'])
   

#     onboarded_user = SelectField('Select Company', choices=user_list, validators=[DataRequired()])
#     allocate_slot = SubmitField=('Allocate Slot')