from flask import Flask, render_template, url_for, request, redirect, session, flash, g, jsonify
from datetime import datetime

from dateutil.relativedelta import relativedelta

import random
import string


from passlib.hash import sha256_crypt
from functools import wraps

import form_creation
import lead_train_db
import nexus_launch_DB
import login_db

import sendMail

app = Flask(__name__)

app.secret_key = 'leadTrain252525'




# ******************************************** login ******************************************

# Login required
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username_retailer' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


@app.route("/logout/")
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))


# Login Section
@app.route("/login/")
def login():
    user_exists_flag = False
    if 'username_retailer' in session:
        user_exists_flag = True
        session['page'] = ''
        
        return redirect(url_for('index'))
    else:
        return render_template('login.html', user = '', user_exists = user_exists_flag)


@app.route("/login/attempt", methods=['POST'])
def login_attempt():
    db_id = ''
    db_pass = ''
    retailer_db = ''
    db_auth_data = {}
    active_list = []
    incorrect_pass_flag = False

    login_id = request.form['e_mail'].strip()
    print(login_id)
    login_pass = request.form['pass_word'].strip()
    
    cursor = login_db.search_authorization_by_id(login_id)
    for c in cursor:
        db_auth_data = c

    dealer_id = db_auth_data["org_id"]
    active_cur = login_db.get_account_activation_status_details(dealer_id)
    for d in active_cur:
        active_list.append(d)

    if db_auth_data:
        if sha256_crypt.verify(login_pass, db_auth_data['password']):
            if active_list:
                session['username_retailer'] = db_auth_data['first_name']
                print(session['username_retailer'])
                session['fullname_retailer'] = db_auth_data['first_name'] + " " + db_auth_data['last_name']
                session['org_retailer'] = db_auth_data['org_name']
                session['email_retailer'] = db_auth_data['user_email']
                session['userId_retailer'] = db_auth_data['user_id']
                session['userType_retailer'] = db_auth_data['user_type']
                session['orgId_retailer'] = db_auth_data['org_id']
                session['phonenum_retailer'] = db_auth_data['user_contact']
                session.pop('_flashes', None)
            else:
                incorrect_pass_flag = True
                return render_template('login.html', incorrect_pass_flag = incorrect_pass_flag)
        else:
            incorrect_pass_flag = True
            return render_template('login.html', incorrect_pass_flag = incorrect_pass_flag)
    else:
        incorrect_pass_flag = True
        return render_template('login.html', incorrect_pass_flag = incorrect_pass_flag)
    return redirect(url_for('login'))

 


 


#======================================================Profile DATA====================================================

@app.route("/profile_info", methods=['GET'])
@login_required
def profileWrapper():
    dealers_info = []
    emp_info = []
    
    dealer_cursor = DOL_DB.get_dealer_basic_details_from_dealer_account()
    for dea in dealer_cursor:
        dealers_info.append(dea)
    print(dealers_info)

    emp_cursor = DOL_DB.get_dealer_basic_details_from_employee_account()
    for emp in emp_cursor:
        emp_info.append(emp)
    print(emp_info)
    return render_template('profile_page.html',
                            dealers_info = dealers_info,
                            emp_info = emp_info,
                            user = session['username_retailer'],
                            org = session['org_retailer'])

# ******************************************* Id generator ****************************************

def generate_prod_id(letters_count, digits_count):
    sample_str = ''.join((random.choice(string.ascii_uppercase) for i in range(letters_count)))
    sample_str += ''.join((random.choice(string.digits) for i in range(digits_count)))
    sample_list = list(sample_str)
    final_string = ''.join(sample_list)
    return final_string

def generate_prod_id_fixL(letters, digits_count):
    sample_str = letters
    sample_str += ''.join((random.choice(string.digits) for i in range(digits_count)))
    sample_list = list(sample_str)
    final_string = ''.join(sample_list)
    return final_string

# **********************************************************************************************



# ===============================================================================================

@app.route('/')
@login_required
def index():
    return redirect(url_for('dashboard'))




@app.route('/dashboard')
@login_required
def dashboard():
    session['page'] = 'dash'
    vip_list = []

    vip_c = lead_train_db.get_vipUsers_count()
    vipUsers_count = len(list(vip_c[0]))
    onBoardedUsers_count = len(list(vip_c[1]))
       
    get_p_count = lead_train_db.get_all_products()
    products_count = len(list(get_p_count))
    
    get_all_vips = lead_train_db.get_all_VIP()
    for v in get_all_vips:
        vip_list.append(v)
        
    return render_template('dashboard.html', 
                            vip_count = vipUsers_count, 
                            onboarded_count= onBoardedUsers_count, 
                            prod_count = products_count, 
                            vip_list = vip_list,                             
                            user = session['username_retailer'])



@app.route('/innerPage_template')
@login_required
def innerPage_template():
    session['page'] = 'blank'
    return render_template('inner_page.html')



def get_all_prods():    
    all_prod_list = []
    cursor = lead_train_db.get_all_products()

    for prods in cursor:
        all_prod_list.append(prods)

    return all_prod_list


@app.route('/product')
@login_required
def product():
    
    session['page'] = 'product'
    prod_form = form_creation.product_form()
    formclass = 'form-control'
    
    all_prod_list = get_all_prods()

    return render_template('product.html', p_form = prod_form, f_class = formclass, all_prod_list = all_prod_list)

@app.route('/trainer')
@login_required
def trainer():
    session['page'] = 'trainer'
    trainer_list = []
    trainer_form = form_creation.trainer_form()
    input_class = 'form-control'

    t_list = lead_train_db.get_trainers()

    if t_list:
        for t in t_list:
            trainer_list.append(t)

     
    # trainers_list = 
    return render_template('trainer_management.html', t_form = trainer_form, input_class = input_class, trainer_list=trainer_list)

@app.route('/save_trainer', methods=['POST'])
@login_required
def save_trainer():
    trainer_info = {}
    selected_country_state = {}

    if request.form.get('country_1'):
        selected_country_state['country'] = 'Canada'
        selected_country_state['state'] = request.form['ca_States']

    elif request.form.get('country_2'):
        selected_country_state['country'] = 'US'
        selected_country_state['state'] = request.form['us_States']       
    

    t_id = generate_prod_id_fixL('NFS_TRNR_', 3)
    print('fixed letter id - ', t_id)
    trainer_info['trainer_id'] = t_id
    trainer_info['first_name'] = request.form['trainer_f_name']
    trainer_info['last_name'] = request.form['trainer_l_name']
    trainer_info['designation'] = request.form['designation']
    trainer_info['email_id'] = request.form['email_id']
    trainer_info['Contact_num'] = request.form['c_num']
    
    if selected_country_state['country']:
        trainer_info['country'] = selected_country_state['country']
    else:
        trainer_info['country'] = ''        
    
    if selected_country_state['state']:
        trainer_info['state'] = selected_country_state['state']
    else:
        trainer_info['state'] = ''

    trainer_info['city'] = request.form['city']

    prod = request.form['nexus_product'].split('_')

    trainer_info['product'] = prod[2]

    trainer_info['trainer_registration_date'] = datetime.today().strftime("%b-%d-%Y")

    print('trainer --------------------------------')
    print(trainer_info)

    lead_train_db.insert_trainer(trainer_info)

    return redirect(url_for('trainer'))

@app.route('/save_product', methods=['POST'])
@login_required
def save_product():
    prod_dict = {}

    prod_dict['Product_id'] = generate_prod_id(3, 4)
    prod_dict['Product_name'] = request.form['prod_name']
    prod_dict['Product_Price'] = request.form['prod_price']
    prod_dict['Product_Creation_Date'] = datetime.today().strftime("%b-%d-%Y")

    lead_train_db.insert_product(prod_dict)

    return redirect(url_for('product'))




@app.route('/approve/<po_id>', methods=['POST'])
@login_required
def approve(po_id):
    status = 'approved'
    apprv_date = datetime.today().strftime("%b-%d-%Y")
    # next_mnth = datetime.today() + relativedelta(months=+2)
    # next_month = next_mnth.strftime("%B")
    # print('next month - ', next_month)
    lead_train_db.update_preorder_status(po_id, status, apprv_date)
    return redirect(url_for('inQueue'))



@app.route('/reject/<po_id>', methods=['POST'])
@login_required
def reject(po_id):
    status = 'rejected'
    reject_date = datetime.today().strftime("%b-%d-%Y")
    lead_train_db.update_preorder_status(po_id, status, reject_date)
    return redirect(url_for('inQueue'))

@app.route('/edit_unpaid/<po_id>')
@login_required
def edit_unpaid(po_id):
    up_user_cursor = lead_train_db.get_unpaid_userInfo(po_id)
    return redirect(url_for('dashboard'))


@app.route('/processed')
@login_required
def processed():
    session['page'] = 'processed'
    trainer_list = []
    vip_list = []

    get_vipList = lead_train_db.get_approved_vipList()    
    get_trainersList = lead_train_db.get_trainers()

    for vl in get_vipList:
        vip_list.append(vl)

    for tl in get_trainersList:
        trainer_list.append(tl)

    print('==========================================')
    print(vip_list)
    return render_template('processed.html', vip_list = vip_list, all_trainer = trainer_list)

@app.route('/inQueue')
@login_required
def inQueue():
    session['page'] = 'iQ'
    comm_log = []
    vip_list = []
    get_vipList = lead_train_db.get_vipList()
    for vip in get_vipList:
        vip_list.append(vip)

    get_inQ_com_data = lead_train_db.get_inQue_comm_data()
    
    for comm in get_inQ_com_data:
        comm_log.append(comm)

    return render_template('inQueue.html', all_vips = vip_list, comm_log = comm_log)
 

@app.route('/on_boarding')
@login_required
def on_boarding():
    vipList = []
    trainer_list = []
    session['page'] = 'on_boarding'

    # onboarded_users = form_creation.slot_alotment()

    # get_vipList = lead_train_db.get_onboarded_client()
    get_onboard_list = lead_train_db.get_approved_vipList()

    for v in get_onboard_list:
        if v['onboarded'] == True:
            vipList.append(v)

    # for t in get_onboard_info:
    #     trainer_list.append(t)

    print('===================')
    print(vipList)
    # return render_template('on_boarding.html', onboarded = vipList, allTrainers = trainer_list, ob_users = onboarded_users)
    return render_template('on_boarding.html', onboarded = vipList)


@app.route('/registration')
@login_required
def registration():
    session['page'] = 'reg'
    reg_data = nexus_launch_DB.get_registration_meeting_data()
    return render_template('registration.html', reg_data=reg_data)


@app.route('/send_confirmation_mail/<email_id>/<comp_name>', methods=['POST'])
@login_required
def send_confirmation_mail(email_id, comp_name):
    mail_data = {}
    mail_data['company_name'] = comp_name
    mail_data['communication_id'] = generate_prod_id_fixL('NFS_COMM_', 5)
    mail_data['mail_id'] = email_id
    mail_data['subject'] = request.form['subject'].strip()
    mail_data['message'] = request.form['cmnt'].strip()
    mail_data['communication_date'] = datetime.today().strftime("%b-%d-%Y")

    print('-----------------------send confirmation')
    print(mail_data)

    sendMail.send_to_mail(mail_data)

    lead_train_db.save_comm_details(mail_data)

    return redirect(url_for('inQueue'))

@app.route('/onboard/<preorder_id>', methods=['POST'])
@login_required
def onboard(preorder_id):
    onboarding_info = {}
    ob_company_info = []
    trainer_info = []
    vip_list_update = {}

    ob_company_info_cursor = lead_train_db.get_approved_vipList_comp_id(preorder_id)

    for ci in ob_company_info_cursor:
        ob_company_info.append(ci)     

    ob_time = request.form['ob_time_hr'] + ':' + request.form['ob_time_mnt'] + ' ' + request.form['ob_time_prt']
    trainer_id = request.form['trainer']
    
    get_trainer_cursor = lead_train_db.get_trainer_info(trainer_id)

    for t in get_trainer_cursor:
        trainer_info.append(t)

    for ti in trainer_info:
        f_name = ti['first_name']
        l_name = ti['last_name']
        desg = ti['designation']
        address = ti['city'] + ', '+ti['state']+ ', ' + ti['country']
        email = ti['email_id']

    onboarding_info['preOrder_id'] = preorder_id
    onboarding_info['company'] = ob_company_info[0]['company_name']
    # onboarding_info['email_id'] = ob_company_info[0]['email_id']
    onboarding_info['product'] = ob_company_info[0]['product_name']
    onboarding_info['onboard_date'] = request.form['ob_date']
    onboarding_info['onboard_time'] = ob_time
    onboarding_info['onboard_scheduled'] = True
    onboarding_info['trainer_name'] = f_name +' '+l_name
    onboarding_info['trainer_id'] = trainer_id
    onboarding_info['estimated_delivery_month'] = ob_company_info[0]['estimated_delivery_month']
    # onboarding_info['designation'] = desg
    # onboarding_info['trainer_address'] = address
    # onboarding_info['trainer_assigned_date'] = datetime.today().strftime("%b-%d-%Y")
    # onboarding_info['training_slot_status'] = 'Not provided'
    # onboarding_info['training_slot'] = {}

    lead_train_db.save_onboarding_info(onboarding_info)

    vip_list_update['onboarded'] = True
    vip_list_update['onboard_date'] = request.form['ob_date']
    vip_list_update['onboard_time'] = ob_time
    # vip_list_update['onboard_scheduled'] = True
    vip_list_update['trainer_assigned'] = True
    vip_list_update['preOrder_id'] = preorder_id
    vip_list_update['trainer_id'] = trainer_id
    vip_list_update['trainer_name'] = f_name +' '+l_name
    vip_list_update['trainer_address'] = address
    vip_list_update['trainer_assigned_date'] = datetime.today().strftime("%b-%d-%Y")
    vip_list_update['designation'] = desg
    vip_list_update['trainer_mail_id'] = email

    sendMail.alert_trainer(vip_list_update, onboarding_info)

    lead_train_db.update_vipList(vip_list_update)

    return redirect(url_for('processed'))


@app.route('/allocate_slot/<po_id>', methods=['POST'])
def allocate_slot(po_id):

    slot_allocation_data = {}
    
    s_hr = request.form['slot_hr']
    s_mnt = request.form['slot_mnt']
    s_period = request.form['slot_period']

    e_hr = request.form['end_slot_hr']
    e_mnt = request.form['end_slot_mnt']
    e_period = request.form['end_slot_period']

    start_date = request.form['training_date']
    start_time = s_hr +':'+ s_mnt + ' ' + s_period

    end_date = request.form['training_end_date']
    end_time = e_hr +':'+ e_mnt + ' ' + e_period

    slot_allocation_data['preOrder_id'] = po_id
    slot_allocation_data['training_start_date_time'] = start_date + ' ' + start_time
    slot_allocation_data['training_end_date_time'] = end_date + ' ' + end_time
    slot_allocation_data['training_slot_status'] = 'Allocated'
    slot_allocation_data['training_slot_assigned_date'] = datetime.today().strftime("%b-%d-%Y")
    slot_allocation_data['training_slot_assigned'] = True

    print('allocation ----------------')
    print(slot_allocation_data)

    lead_train_db.update_slot(slot_allocation_data)
    return redirect(url_for('on_boarding'))



@app.route('/trainer_profile/<trainer_id>')
def trainer_profile(trainer_id):
    details = []
    trainer_details = lead_train_db.get_trainer_info(trainer_id)

    for td in trainer_details:
        details.append(td)

    return render_template('trainer_profile.html', trainer_info = details)
# ==================================================================
# ====================================================================================

@app.route('/addFields')
@login_required
def addFields():
    lead_train_db.addFields()
    return redirect(url_for('dashboard'))

# =========================================================================
# ====================================================================================================

if __name__ == '__main__':
    app.run(debug=True)