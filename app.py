from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from flask import json

import requests
import csv

from user import *
from password_reset import *
from profiles import *
from activation import *
from account_type import *
from trade_config import *
from banks import *
from customer import *
from loan import *
# from saving import *
from gl import *
from banks import *
from equities import *
from equities_charges import *
from equities_stocks import *
from equities_transactions import *
from etfs import *
from etfs_charges import *
from etfs_stocks import *
from etfs_transactions import *
from treasury import *
from transactions import *
from database import *
import random


# generate random transaction ref
def generateTransactionCode():
    randNum = random.random()
    randToString = str(randNum)
    filteredNum = randToString[9:]
    return filteredNum

# index
@app.route('/')
def index():
    data = {
        'status': 'success',
        'message': 'Welcome to tridex api'
    }

    return jsonify(data)


# index
@app.route('/setup/account')
def setup_accounts():
    account_types = ['Deposit Account', 'Cash Account', 'Bank Account', 'Loan Account', 'Expense Account', 'Investment Account', 'Saving Account', 'Equity', 'Bonds', 'Tbills', 'ETFs']
    for account in account_types:
        AccountType.add_account_type(account)

    data = {
        'status': 'success',
        'message': 'Account setups completed!'
    }

    return jsonify(data)

#--------------------------------------------------
# USER AND AUTHENTICATION ENDPOINT 
# create new user
#--------------------------------------------------
@app.route('/auth/signup', methods=['POST'])
def signup_user():
    signup_payload = request.get_json()
    user_name = signup_payload['name']
    user_email = signup_payload['email']
    user_password = signup_payload['password']
    user_avatar = signup_payload['avatar']

    User.add_user(user_name, user_email, user_password, user_avatar)
    activation_link = Activation.init_user_activation(user_email)

    # init system default account
    user = User.query.filter_by(email=user_email).first()
    Profile.init_user_profile(user.id)
    Gl.init_gl_account(user.id, 1)
    Bank.init_user_bank(user.id)

    data = {
        'status': 'success',
        'message': 'Account activation link has been sent to '+signup_payload['email'],
        'activation_link': activation_link
    }

    status = 201
    
    # return response
    response = Response(json.dumps(data), status, mimetype='application/json')
    return response

@app.route('/init/system/accounts/<int:user_id>', methods=['POST'])
def init_system_account(user_id):
    # create default GL Account
    Profile.init_user_profile(user_id)
    Gl.init_gl_account(user_id, 1)
    Bank.init_user_bank(user_id)

    data = {
        'status': 'success',
        'message': 'Default system accounts has been created successfully!'
    }

    status = 201
    
    # return response
    response = Response(json.dumps(data), status, mimetype='application/json')
    return response

# fetch all users
@app.route('/auth/users')
def all_users():
	data = User.get_all_users()

	# return response
	response = Response(json.dumps(data), 200, mimetype='application/json')
	return response

# login new user
@app.route('/auth/signin', methods=['POST'])
def signin_user():
    signin_payload = request.get_json()
    login_user = User.authenticate_user(signin_payload['email'], signin_payload['password'])
    data = {}
    if(login_user):
    	user_data = User.get_user_by_email(signin_payload['email'])
    	data = {
    		'status': 'success',
    		'message': 'Login successful!',
    		'data': user_data
    	}
    else:
    	data = {
    		'status': 'error',
    		'message': 'Invalid login credentials'
    	}

    # return response
    response = Response(json.dumps(data), 200, mimetype='application/json')
    return response

# activate new user
@app.route('/auth/activate')
def activate_user():
    activation_link = request.args.get('link')
    data = Activation.activate_account(activation_link);

    # return response
    response = Response(json.dumps(data), 200, mimetype='application/json')
    return response

# get user by username
@app.route('/auth/user/<int:user_id>')
def get_user_by_id(user_id):
    data = User.get_user_by_user_id(user_id)

    # return response
    response = Response(json.dumps(data), 200, mimetype='application/json')
    return response

# get user by username
@app.route('/user/<string:email>')
def get_user(email):
	data = User.get_user_by_email(email)

	# return response
	response = Response(json.dumps(data), 200, mimetype='application/json')
	return response

# get user by email
@app.route('/auth/verify-email', methods=['POST'])
def auth_verify_email():
    reset_data = request.get_json()
    email = reset_data['email']
    data = User.verify_email_exist(email)
    if(data['status'] == "success"):
        PasswordReset.addOne(email, data['reset_link']);
        print('save reset link')

    # return response
    response = Response(json.dumps(data), 200, mimetype='application/json')
    return response

# update user avatar
@app.route('/user/avatar/<int:id>', methods=['PUT'])
def replace_user_avatar(id):
    user_data = request.get_json()
    User.update_user_avatar(id, user_data['avatar'])

    data = {
        "status": "success",
        "message": "Your profile has been updated successfully!"
    }

    # return response
    response = Response(json.dumps(data), 200, mimetype='application/json')
    return response

# update user name
@app.route('/user/name/<int:id>', methods=['PUT'])
def replace_user_name(id):
    user_data = request.get_json()
    data = User.update_user_name(id, user_data['name'])

    # return response
    response = Response(json.dumps(data), 200, mimetype='application/json')
    return response

# reset user password
@app.route('/user/reset/<string:email>', methods=['PUT'])
def reset_user_password(email):
    user_data = request.get_json()
    data = User.update_user_password(email, user_data['password'])

# change user password
@app.route('/user/password/<int:user_id>', methods=['PUT'])
def change_user_password(user_id):
    user_data = request.get_json()
    old_password = user_data['old_password']
    new_password = user_data['new_password']
    if(User.change_user_password(user_id, old_password, new_password)):
        data = {
            "status": "success",
            "message": "Password updated successful!"
        }
    else:
        data = {
            "status": "error",
            "message": "Invalid password, try again!"
        }

    # return response
    response = Response(json.dumps(data), 200, mimetype='application/json')
    return response


#--------------------------------------------------
# CUSTOMER ACCOUNT AND SETUP ENDPOINT 
# create new customer account
#--------------------------------------------------
@app.route('/customer/add', methods=['POST'])
def add_customer():
    customer_payload = request.get_json()
    full_name = customer_payload['full_name']
    acct_code = customer_payload['acct_code']
    passport = customer_payload['passport']
    bvn = customer_payload['bvn']
    email = customer_payload['email']
    state_of_origin = customer_payload['state_of_origin']
    gender = customer_payload['gender']
    local_govt = customer_payload['local_govt']
    date_of_birth = customer_payload['date_of_birth']
    nationality = customer_payload['nationality']
    phone_number = customer_payload['phone_number']
    occupation = customer_payload['occupation']
    description = customer_payload['description']
    home_address = customer_payload['home_address']
    business_address = customer_payload['business_address']

    Customer.add_customer(passport, full_name, acct_code, bvn, email, state_of_origin, gender, local_govt, date_of_birth, nationality, phone_number, occupation, description, home_address, business_address)

    data = {
        'status': 'success',
        'message': full_name+' has been created successfully!'
    }

    status = 201
    
    # return response
    response = Response(json.dumps(data), status, mimetype='application/json')
    return response

# fetch all account types
@app.route('/customer/all')
def all_customer():
    customers = Customer.all_customer()
    status = 201
    
    # return response
    response = Response(json.dumps(customers), status, mimetype='application/json')
    return response

# fetch customer by id
@app.route('/customer/one/<int:id>')
def one_customer(id):
    customer = Customer.one_customer(id)
    status = 201
    
    # return response
    response = Response(json.dumps(customer), status, mimetype='application/json')
    return response

# update customer by id
@app.route('/customer/one/<int:id>', methods=['PUT'])
def update_customer(id):
    customer_payload = request.get_json()
    full_name = customer_payload['full_name']
    acct_code = customer_payload['acct_code']
    passport = customer_payload['passport']
    bvn = customer_payload['bvn']
    email = customer_payload['email']
    state_of_origin = customer_payload['state_of_origin']
    gender = customer_payload['gender']
    local_govt = customer_payload['local_govt']
    date_of_birth = customer_payload['date_of_birth']
    nationality = customer_payload['nationality']
    phone_number = customer_payload['phone_number']
    occupation = customer_payload['occupation']
    description = customer_payload['description']
    home_address = customer_payload['home_address']
    business_address = customer_payload['business_address']

    customer = Customer.update_customer(id, passport, full_name, acct_code, bvn, email, state_of_origin, gender, local_govt, date_of_birth, nationality, phone_number, occupation, description, home_address, business_address)
    status = 201
    
    # return response
    response = Response(json.dumps(customer), status, mimetype='application/json')
    return response

# delete customer by id
@app.route('/customer/one/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.delete_customer(id)
    status = 204
    
    # return response
    response = Response(json.dumps(customer), status, mimetype='application/json')
    return response

# upload customer list
@app.route('/customer/upload', methods=['POST'])
def upload_customer():
    customer_payload = request.get_json()
    excel_file_name = customer_payload['file_name']
    excel_file_url = customer_payload['file_url']

    excel_file = requests.get(excel_file_url)
    with open('excel/'+excel_file_name, 'wb') as f:
        f.write(excel_file.content)


    with open('excel/'+excel_file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                full_name = row[0]
                bvn = row[1]
                email = row[2]
                state_of_origin = 23 # Default lagos
                gender = row[4]
                local_govt = 1 # Default Ajeromi
                date_of_birth = row[6]
                nationality = 1 # Default Nigeria
                phone_number = row[8]
                occupation = 8 # Default business
                description = row[10]
                home_address = row[11]
                business_address = row[12]
                acct_code = row[13]
                passport = "http://localhost:3300/img/avatar.png"

                Customer.add_customer(passport, full_name, acct_code, bvn, email, state_of_origin, gender, local_govt, date_of_birth, nationality, phone_number, occupation, description, home_address, business_address)

                line_count += 1

    data = {
        'status': 'success',
        'message': excel_file_name + ' File has been created successfully!'
    }

    status = 201
    
    # return response
    response = Response(json.dumps(data), status, mimetype='application/json')
    return response


#--------------------------------------------------
# LOAN TYPE AND SETUP ENDPOINT 
# create new LOAN type
#--------------------------------------------------
@app.route('/loan/add', methods=['POST'])
def add_loan():
    loan_payload = request.get_json()
    customer_id = loan_payload['customer_id']
    principal = loan_payload['principal']
    interest = loan_payload['interest']
    amount = loan_payload['amount']
    daily_payment = loan_payload['daily_repayment']
    weekly_payment = loan_payload['weekly_repayment']
    monthly_payment = loan_payload['monthly_repayment']
    daily_duration = loan_payload['duration_in_days']
    weekly_duration = loan_payload['duration_in_weeks']
    monthly_duration = loan_payload['duration_in_months']
    percentage = loan_payload['percentage']
    type_of_loan = 1
    loan_start_date = loan_payload['loan_start_date']
    loan_end_date = loan_payload['loan_end_date']
    status = 1

    # add user equity account not exist!
    loan_account_type_id = 4
    Gl.add_new(customer_id, loan_account_type_id, "Loan Ledger")
    customer_gl = Gl.get_user_gl_by_type(customer_id, loan_account_type_id)
    gl_id = customer_gl['id']

    # loan description
    description = "#"+generateTransactionCode()+" Loan Ledger"

    Loan.add_loan(customer_id, description, principal, interest, amount, daily_payment, weekly_payment, monthly_payment, daily_duration, weekly_duration, monthly_duration, percentage, gl_id, status, type_of_loan, loan_start_date, loan_end_date)

    data = {
        'status': 'success',
        'message': 'Loan has been created successfully!'
    }

    status = 201
    
    # return response
    response = Response(json.dumps(data), status, mimetype='application/json')
    return response

# fetch all account types
@app.route('/loan/all')
def all_loan():
    all_loans = Loan.all_loan()
    status = 201
    
    # return response
    response = Response(json.dumps(all_loans), status, mimetype='application/json')
    return response

# fetch account type by id
@app.route('/loan/one/<int:id>')
def one_loan(id):
    loan = Loan.one_loan(id)
    status = 201
    
    # return response
    response = Response(json.dumps(loan), status, mimetype='application/json')
    return response

# update account type by id
@app.route('/loan/one/<int:id>', methods=['PUT'])
def update_loan(id):
    loan_payload = request.get_json()
    account_type = Loan.update_loan(id, loan_payload['status'])
    status = 204
    
    # return response
    response = Response(json.dumps(account_type), status, mimetype='application/json')
    return response

# delete account type by id
@app.route('/loan/one/<int:id>', methods=['DELETE'])
def delete_loan(id):
    loan = Loan.delete_loan(id)
    status = 204
    
    # return response
    response = Response(json.dumps(loan), status, mimetype='application/json')
    return response



#--------------------------------------------------
# TRADE CONFIGURATION TYPE AND SETUP ENDPOINT 
# init trade config
#--------------------------------------------------
@app.route('/trade/config')
def trade_config_fetch_all():
    trade_config = TradeConfig.fetch_all()

    status = 200

    # return response
    response = Response(json.dumps(trade_config), status, mimetype='application/json')
    return response

@app.route('/trade/config/<int:id>')
def trade_config_fetch_one(id):
    trade_config = TradeConfig.fetch_one(id)

    status = 200

    # return response
    response = Response(json.dumps(trade_config), status, mimetype='application/json')
    return response

@app.route('/trade/config', methods=['POST'])
def trade_config_add_new():
    trade_config_data = request.get_json()
    TradeConfig.add_new(trade_config_data['name'])

    status = 201

    data = {
        "status": "success",
        "message": trade_config_data['name'] + " added!"
    }

    # return response
    response = Response(json.dumps(data), status, mimetype='application/json')
    return response

@app.route('/trade/config/<int:id>', methods=['PUT'])
def trade_config_update_data(id):
    trade_config_data = request.get_json()
    TradeConfig.update_config(id, trade_config_data['name'])

    status = 204

    data = {
        "status": "success",
        "message": trade_config_data['name'] + " updated!"
    }

    # return response
    response = Response(json.dumps(data), status, mimetype='application/json')
    return response

@app.route('/trade/config/<int:id>', methods=['DELETE'])
def trade_config_delete_data(id):
    TradeConfig.delete_config(id)

    status = 204

    data = {
        "status": "success",
        "message": trade_config_data['name'] + " deleted!"
    }

    # return response
    response = Response(json.dumps(data), status, mimetype='application/json')
    return response



#--------------------------------------------------
# BANKS SETUP FOR CLIENT ENDPOINT
# init bank endpoint
#--------------------------------------------------
@app.route('/bank/<int:user_id>', methods=['PUT'])
def update_user_bank(user_id):
    bank_data = request.get_json()
    number = bank_data['number']
    sort_code = bank_data['sort_code']
    bank_name = bank_data['bank_name']
    owner_name = bank_data['owner_name']
    bank = Bank.update_user_bank(user_id, number, sort_code, bank_name, owner_name)

    # return response
    response = Response(json.dumps(bank), 204, mimetype='application/json')
    return response

@app.route('/bank/<int:user_id>')
def get_user_bank(user_id):
    bank = Bank.get_bank_by_user_id(user_id)

    # return response
    response = Response(json.dumps(bank), 200, mimetype='application/json')
    return response


#--------------------------------------------------
# USER PROFILE SETUP ENDPOINT 
# init profile endpoint
#--------------------------------------------------
@app.route('/profile/<int:user_id>')
def fetch_single_profile(user_id):
    user_profile = Profile.get_user_profile(user_id)

    # return response
    response = Response(json.dumps(user_profile), 200, mimetype='application/json')
    return response

@app.route('/profile/<int:user_id>', methods=["PUT"])
def update_single_profile(user_id):
    profile_data = request.get_json()
    gender = profile_data['gender']
    bvn = profile_data['bvn']
    phone = profile_data['phone']
    address = profile_data['address']
    occupation = profile_data['occupation']
    date_of_birth = profile_data['date_of_birth']
    state_of_origin = profile_data['state_of_origin']
    lga = profile_data['lga']
    nationality = profile_data['nationality']
    description = profile_data['description']

    # update user profile
    Profile.update_user_profile(user_id, gender, bvn, phone, address, occupation, date_of_birth, state_of_origin, lga, nationality, description)

    data = {
        "status": "success",
        "message": "Update successful!"
    }

    # return response
    response = Response(json.dumps(data), 200, mimetype='application/json')
    return response



#--------------------------------------------------
# EQUITIES SETUP ENDPOINT
# init equity endpoint
#--------------------------------------------------
@app.route('/equity')
def get_all_equity():
    equities = Equity.get_all()
    status = 200

    # return response
    response = Response(json.dumps(equities), status, mimetype='application/json')
    return response

@app.route('/equity', methods=["POST"])
def add_new_equity():
    equity_data = request.get_json()
    security = equity_data["security"]
    market = equity_data["market"]
    sector = equity_data["sector"]
    previous_closing_price = equity_data["previous_closing_price"]
    open_price = equity_data["open_price"]
    close_price = equity_data["close_price"]

    equity = Equity.add_new(security, market, sector, previous_closing_price, open_price, close_price)
    status = 200
    
    # return response
    response = Response(json.dumps(equity), status, mimetype='application/json')
    return response

@app.route('/equity/<int:id>', methods=["PUT"])
def update_equity(id):
    equity_data = request.get_json()
    market = equity_data["market"]
    sector = equity_data["sector"]
    previous_closing_price = equity_data["previous_closing_price"]
    open_price = equity_data["open_price"]
    close_price = equity_data["close_price"]

    equities = Equity.update_equity(id, market, sector, previous_closing_price, open_price, close_price)
    status = 200
    
    # return response
    response = Response(json.dumps(equities), status, mimetype='application/json')
    return response

@app.route('/equity/price/<int:id>', methods=["PUT"])
def update_equity_open_price(id):
    equity_data = request.get_json()
    open_price = equity_data["open_price"]

    data = Equity.update_equity_open_price(id, open_price)
    status = 200
    
    # return response
    response = Response(json.dumps(data), status, mimetype='application/json')
    return response

@app.route('/equity/<int:id>')
def get_one_equity(id):
    equity = Equity.get_equity_by_id(id)
    status = 200

    # return response
    response = Response(json.dumps(equity), status, mimetype='application/json')
    return response

@app.route('/equity/symbol/<string:symbol>')
def get_one_by_symbol(symbol):
    equity = Equity.get_equity_by_name(symbol)
    status = 200

    # return response
    response = Response(json.dumps(equity), status, mimetype='application/json')
    return response


#--------------------------------------------------
# EQUITIES CHARGES SETUP ENDPOINT
# init equity endpoint
#--------------------------------------------------
@app.route('/equity_charges')
def get_all_equity_charges():
    equities_charges = EquityCharge.get_all()
    status = 200

    # return response
    response = Response(json.dumps(equities_charges), status, mimetype='application/json')
    return response

@app.route('/equity_charges', methods=["POST"])
def add_new_equity_charge():
    equity_data = request.get_json()
    name = equity_data["name"]
    rate = equity_data["rate"]
    vat = equity_data["vat"]
    total = equity_data["total"]
    trade_type = equity_data["trade_type"]

    equity = EquityCharge.add_new(name, rate, vat, total, trade_type)
    status = 200

    # required account
    
    # return response
    response = Response(json.dumps(equity), status, mimetype='application/json')
    return response

@app.route('/equity_charges/<int:id>', methods=["PUT"])
def update_equity_charge(id):
    equity_data = request.get_json()
    name = equity_data["name"]
    rate = equity_data["rate"]
    vat = equity_data["vat"]
    total = equity_data["total"]
    trade_type = equity_data["trade_type"]

    equity = EquityCharge.update_equity_charge(id, name, rate, vat, total, trade_type)
    status = 200
    
    # return response
    response = Response(json.dumps(equity), status, mimetype='application/json')
    return response

@app.route('/equity_charges/<int:id>')
def get_one_equity_charge(id):
    equity = EquityCharge.get_equity_charge_by_id(id)
    status = 200

    # return response
    response = Response(json.dumps(equity), status, mimetype='application/json')
    return response

@app.route('/equity_charges/<int:id>', methods=['DELETE'])
def delete_one_equity_charge(id):
    equity = EquityCharge.delete_equity_charge(id)
    status = 200

    # return response
    response = Response(json.dumps(equity), status, mimetype='application/json')
    return response


#--------------------------------------------------
# General Ledger SETUP ENDPOINT
# init gl endpoint
#--------------------------------------------------
@app.route('/gls')
def get_all_gl():
    gls = Gl.get_all()

    all_gls = []
    for gl in gls:
        gl['account_type'] = AccountType.fetch_one_account(gl['account_type_id'])
        all_gls.append(gl);

    status = 200

    # return response
    response = Response(json.dumps(all_gls), status, mimetype='application/json')
    return response

@app.route('/gls', methods=["POST"])
def add_new_gl():
    gl_data = request.get_json()
    user_id = gl_data["user_id"]
    description = gl_data["description"]
    account_type_id = gl_data["account_type_id"]
    Gl.add_new(user_id, account_type_id, description)

    data = {
        "status": "success",
        "message": "GL account created successfully!"
    }
    status = 200
    
    # return response
    response = Response(json.dumps(data), status, mimetype='application/json')
    return response

@app.route('/gls/<int:id>', methods=["PUT"])
def update_gl(id):
    gl_data = request.get_json()
    gl_id = gl_data["gl_id"]
    description = gl_data["description"]
    account_type_id = gl_data["account_type_id"]

    gl = Gl.update_one(gl_id, description)
    status = 200
    
    # return response
    response = Response(json.dumps(gl), status, mimetype='application/json')
    return response

@app.route('/gls/<int:user_id>')
def get_one_gl(user_id):
    gl = Gl.get_all_user_gl(user_id)
    status = 200

    # return response
    response = Response(json.dumps(gl), status, mimetype='application/json')
    return response

@app.route('/gls/<int:user_id>/<int:account_type_id>')
def get_user_gl(user_id, account_type_id):
    gl = Gl.get_user_gl_by_type(user_id, account_type_id)
    status = 200

    # return response
    response = Response(json.dumps(gl), status, mimetype='application/json')
    return response


#--------------------------------------------------
# POST TRANSACTIONS
# init transactions endpoint
#--------------------------------------------------
@app.route('/transaction')
def get_all_transactions():
    all_transactions = Transaction.get_all()
    status = 200

    # return response
    response = Response(json.dumps(all_transactions), status, mimetype='application/json')
    return response

@app.route('/transaction/<int:user_id>')
def get_all_user_transactions(user_id):
    all_transactions = Transaction.get_all_by_user_id(user_id)
    status = 200

    # return response
    response = Response(json.dumps(all_transactions), status, mimetype='application/json')
    return response

@app.route('/transaction/<int:user_id>/<int:account_type_id>')
def get_all_user_transactions_by_gl(user_id, account_type_id):
    user_gl_account = Gl.get_user_gl_by_type(user_id, account_type_id);
    all_transactions = Transaction.get_all_by_user_id_and_gl_id(user_id, user_gl_account['id'])
    status = 200

    # return response
    response = Response(json.dumps(all_transactions), status, mimetype='application/json')
    return response

@app.route('/transaction/posting/<string:reference>')
def get_all_transactions_by_reference(reference):
    amount = request.args.get('amount')
    all_transactions = Transaction.get_all_by_reference(reference, amount)
    status = 200

    # return response
    response = Response(json.dumps(all_transactions), status, mimetype='application/json')
    return response

@app.route('/transaction/gl/<int:gl_id>')
def get_all_transactions_by_gl(gl_id):
    all_transactions = Transaction.get_transaction_by_gl_id(gl_id)
    status = 200

    # return response
    response = Response(json.dumps(all_transactions), status, mimetype='application/json')
    return response

@app.route('/transaction', methods=["POST"])
def add_new_transaction():
    transaction_data = request.get_json()
    reference = generateTransactionCode()
    account_type_id = transaction_data['account_type_id']
    amount = transaction_data['amount']
    user_id = transaction_data['user_id']
    narration = transaction_data['narration'] 

    user_account = Gl.get_user_gl_by_type(user_id, account_type_id)
    gl_id = user_account['id']

    system_user_id = 1
    system_cash_gl = 1

    # process debit and credit transaction
    Transaction.debit(system_user_id, system_cash_gl, amount, narration, reference)
    Transaction.credit(user_id, gl_id, amount, narration, reference)

    data = {
        "status": "success",
        "message": "Transaction successful!"
    }
    status = 200
    
    # return response
    response = Response(json.dumps(data), status, mimetype='application/json')
    return response

@app.route('/transaction/equity', methods=["POST"])
def add_new_equity_transaction():
    transaction_data = request.get_json()
    reference = generateTransactionCode()
    equity_account_type_id = 3

    commission_gl_id = transaction_data["commission_gl_id"]
    cscs_gl_id = transaction_data["cscs_gl_id"]
    sec_gl_id = transaction_data["sec_gl_id"]
    nse_gl_id = transaction_data["nse_gl_id"]
    stamp_duties_gl_id = transaction_data["stamp_duties_gl_id"]

    user_id = transaction_data["user_id"]
    transaction_type = transaction_data["transaction_type"]
    equity_id = transaction_data["equity_id"]
    units = int(transaction_data["units"])

    equity_details = Equity.get_equity_by_id(equity_id)
    open_price = equity_details['open_price']
    
    # add user equity account not exist!
    Gl.add_new(user_id, equity_account_type_id, "Equities Ledger")
    user_account = Gl.get_user_gl_by_type(user_id, equity_account_type_id)
    user_equity_gl_id = user_account['id']

    # add for equity gl account if not exist!
    Gl.add_new(1, equity_account_type_id, "System Equities Ledger")
    system_account = Gl.get_user_gl_by_type(1, equity_account_type_id)
    system_equity_gl_id = system_account['id']

    # instant deposit
    user_deposit_account = Gl.get_user_gl_by_type(user_id, 1);
    deposit_account_balance = Transaction.available_balance(user_id, user_deposit_account['id'])

    if(transaction_type == "1"):
        # process debit and credit transaction
        commission = float(transaction_data["commission"])
        cscs = float(transaction_data["cscs"])
        sec = float(transaction_data["sec"])
        # nse = float(transaction_data["nse"])
        stamp_duties = float(transaction_data["stamp_duties"])

        debit_narration = f"Purchased {units:,} unit(s) of "+ equity_details['security']
        credit_narration = f"Sold {units:,} unit(s) of "+ equity_details['security']

        com_charges_narration = f"Brokerage commission on {units:,} unit(s) of "+ equity_details['security']
        cscs_charges_narration = f"CSCS Fee on {units:,} unit(s) of "+ equity_details['security']
        sec_charges_narration = f"SEC Fee on {units:,} unit(s) of "+ equity_details['security']
        stamp_charges_narration = f"Stamp Duties on {units:,} unit(s) of "+ equity_details['security']
        
        charges = commission + cscs + sec + stamp_duties
        amount = units * open_price + charges
        total = units * open_price

        wa_price = open_price

        if(deposit_account_balance < amount):
            data = {
                "status": "info",
                "message": "Insufficient balance, fund account and try again!"
            }
        elif(deposit_account_balance >= amount):


            Transaction.credit(1, system_equity_gl_id, total, credit_narration, reference)
            Transaction.debit(user_id, user_equity_gl_id, total, debit_narration, reference)

            Transaction.credit(1, commission_gl_id, commission, com_charges_narration, reference)
            Transaction.debit(user_id, user_equity_gl_id, commission, com_charges_narration, reference)

            Transaction.credit(1, cscs_gl_id, cscs, cscs_charges_narration, reference)
            Transaction.debit(user_id, user_equity_gl_id, cscs, cscs_charges_narration, reference)

            Transaction.credit(1, sec_gl_id, sec, sec_charges_narration, reference)
            Transaction.debit(user_id, user_equity_gl_id, sec, sec_charges_narration, reference)

            Transaction.credit(1, stamp_duties_gl_id, stamp_duties, stamp_charges_narration, reference)
            Transaction.debit(user_id, user_equity_gl_id, stamp_duties, stamp_charges_narration, reference)

            # record user stock volume
            EquityStock.add_new(user_id, equity_id, equity_account_type_id, open_price, units, total, wa_price)

            # record user stock transaction
            last_seen_trans = Transaction.get_by_reference_user_id(reference, user_id)
            EquityTransaction.add_new(user_id, equity_id, last_seen_trans['id']);

            data = {
                "status": "success",
                "message": "Transaction successful!"
            }
    elif(transaction_type == "2"):
        # process debit and credit transaction
        commission = float(transaction_data["commission"])
        cscs = float(transaction_data["cscs"])
        # sec = float(transaction_data["sec"])
        nse = float(transaction_data["nse"])
        stamp_duties = float(transaction_data["stamp_duties"])

        debit_narration = "Purchased "+str(units)+" unit(s) of "+ equity_details['security']
        credit_narration = "Sold "+str(units)+" unit(s) of "+ equity_details['security']
        charges = commission + cscs + nse + stamp_duties
        amount = units * equity_details['open_price'] - charges

        Transaction.debit(system_user_id, system_equity_gl_id, amount, debit_narration, reference)
        Transaction.credit(user_id, user_equity_gl_id, amount, credit_narration, reference)

        data = {
            "status": "success",
            "message": "Transaction successful!"
        }

    else:
        data = {
            "status": "error",
            "message": "Invalid transaction type!"
        }

    status = 200
    
    # return response
    response = Response(json.dumps(data), status, mimetype='application/json')
    return response

@app.route('/account/balance/<int:user_id>/<int:account_type_id>')
def get_user_balance(user_id, account_type_id):
    user_account = Gl.get_user_gl_by_type(user_id, account_type_id)
    # user_equity_account = Gl.get_user_gl_by_type(user_id, 3)

    deposit_gl_id = user_account['id']
    # equity_gl_id = user_equity_account['id']

    deposit_account_balance = Transaction.available_balance(user_id, deposit_gl_id)
    # equity_account_balance = Transaction.available_balance(user_id, equity_gl_id)
    net_account_balance = deposit_account_balance

    data = {
        "equity_balance": 0,
        "account_balance": str(net_account_balance)
    }

    status = 200
    
    # return response
    response = Response(json.dumps(data), status, mimetype='application/json')
    return response


#--------------------------------------------------
# STOCK BALANCES
# init stocks endpoint
#--------------------------------------------------
@app.route('/stocks/<int:user_id>')
def get_all_stocks(user_id):
    all_stocks = EquityStock.stocks_balance(user_id)
    status = 200

    # return response
    response = Response(json.dumps(all_stocks), status, mimetype='application/json')
    return response

@app.route('/stock/history/<int:equity_id>')
def get_equity_transaction_history(equity_id):
    equity_transactions = EquityTransaction.get_by_equity_id(equity_id)
    all_transactions = []
    for transaction in equity_transactions:
        equity_transaction = Transaction.get_transaction_by_id(transaction['transaction_id']);
        all_transactions.append(equity_transaction)

    status = 200
    
    # return response
    response = Response(json.dumps(all_transactions), status, mimetype='application/json')
    return response


#--------------------------------------------------
# ETFS SETUP ENDPOINT
# init etf endpoint
#--------------------------------------------------
@app.route('/etfs')
def get_all_etfs():
    equities = Etf.get_all()
    status = 200

    # return response
    response = Response(json.dumps(equities), status, mimetype='application/json')
    return response

@app.route('/etfs', methods=["POST"])
def add_new_etfs():
    etf_data = request.get_json()
    security = etf_data["security"]
    market = etf_data["market"]
    sector = etf_data["sector"]
    previous_closing_price = etf_data["previous_closing_price"]
    open_price = etf_data["open_price"]
    close_price = etf_data["close_price"]

    etf = Etf.add_new(security, market, sector, previous_closing_price, open_price, close_price)
    status = 200
    
    # return response
    response = Response(json.dumps(etf), status, mimetype='application/json')
    return response

@app.route('/etfs/<int:id>', methods=["PUT"])
def update_etf(id):
    etf_data = request.get_json()
    market = etf_data["market"]
    sector = etf_data["sector"]
    previous_closing_price = etf_data["previous_closing_price"]
    open_price = etf_data["open_price"]
    close_price = etf_data["close_price"]

    etfs = Etf.update_etf(id, market, sector, previous_closing_price, open_price, close_price)
    status = 200
    
    # return response
    response = Response(json.dumps(etfs), status, mimetype='application/json')
    return response

@app.route('/etfs/price/<int:id>', methods=["PUT"])
def update_etf_open_price(id):
    etf_data = request.get_json()
    open_price = etf_data["open_price"]

    data = Etf.update_etf_open_price(id, open_price)
    status = 200
    
    # return response
    response = Response(json.dumps(data), status, mimetype='application/json')
    return response

@app.route('/etfs/<int:id>')
def get_one_etf(id):
    etf = Etf.get_etf_by_id(id)
    status = 200

    # return response
    response = Response(json.dumps(etf), status, mimetype='application/json')
    return response

@app.route('/etfs/symbol/<string:symbol>')
def get_etf_by_symbol(symbol):
    etf = Etf.get_etf_by_name(symbol)
    status = 200

    # return response
    response = Response(json.dumps(etf), status, mimetype='application/json')
    return response


#--------------------------------------------------
# ETFS CHARGES SETUP ENDPOINT
# init etfs endpoint
#--------------------------------------------------
@app.route('/etfs_charges')
def get_all_etf_charges():
    etf_charges = EtfCharge.get_all()
    status = 200

    # return response
    response = Response(json.dumps(etf_charges), status, mimetype='application/json')
    return response

@app.route('/etfs_charges', methods=["POST"])
def add_new_etf_charge():
    etf_data = request.get_json()
    name = etf_data["name"]
    rate = etf_data["rate"]
    vat = etf_data["vat"]
    total = etf_data["total"]
    trade_type = etf_data["trade_type"]

    etf = EtfCharge.add_new(name, rate, vat, total, trade_type)
    status = 200

    # required account
    
    # return response
    response = Response(json.dumps(etf), status, mimetype='application/json')
    return response

@app.route('/etfs_charges/<int:id>', methods=["PUT"])
def update_etf_charge(id):
    etf_data = request.get_json()
    name = etf_data["name"]
    rate = etf_data["rate"]
    vat = etf_data["vat"]
    total = etf_data["total"]
    trade_type = etf_data["trade_type"]

    etf = EtfCharge.update_etf_charge(id, name, rate, vat, total, trade_type)
    status = 200
    
    # return response
    response = Response(json.dumps(etf), status, mimetype='application/json')
    return response

@app.route('/etfs_charges/<int:id>')
def get_one_etf_charge(id):
    etf = EtfCharge.get_etf_charge_by_id(id)
    status = 200

    # return response
    response = Response(json.dumps(etf), status, mimetype='application/json')
    return response

@app.route('/etfs_charges/<int:id>', methods=['DELETE'])
def delete_one_etf_charge(id):
    etf = EtfCharge.delete_etf_charge(id)
    status = 200

    # return response
    response = Response(json.dumps(etf), status, mimetype='application/json')
    return response


#--------------------------------------------------
# TREASURY BILL SETUP ENDPOINT
# init treasury endpoint
#--------------------------------------------------
@app.route('/treasury')
def get_all_treasury():
    treasury = Treasury.get_all()
    status = 200

    # return response
    response = Response(json.dumps(treasury), status, mimetype='application/json')
    return response

@app.route('/treasury', methods=["POST"])
def add_new_treasury():
    treasury_data = request.get_json()
    security = treasury_data['security']
    market = treasury_data['market']
    sector = treasury_data['sector']
    product_id = treasury_data['product_id']
    description = treasury_data['description']
    maturity = treasury_data['maturity']
    closing_price = treasury_data['closing_price']
    discount_yield = treasury_data['discount_yield']
    closing_date = treasury_data['closing_date']
    next_close_date = treasury_data['next_close_date']
    closing_mkt_price = treasury_data['closing_mkt_price']
    prev_closing = treasury_data['prev_closing']
    next_closing = treasury_data['next_closing']
    prev_closing_mkt_price = treasury_data['prev_closing_mkt_price']
    next_closing_mkt_price = treasury_data['next_closing_mkt_price']
    EOM_mkt_price = treasury_data['EOM_mkt_price']
    EOY_mkt_price = treasury_data['EOY_mkt_price']
    EOM_date = treasury_data['EOM_date']
    EOY_date = treasury_data['EOY_date']
    prev_business_day = treasury_data['prev_business_day']
    prev_trade_date = treasury_data['prev_trade_date']
    month_start_date = treasury_data['month_start_date']
    year_start_date = treasury_data['year_start_date']
    month_end_date = treasury_data['month_end_date']
    year_end_date = treasury_data['year_end_date']
    cost_of_funds = treasury_data['cost_of_funds']

    treasury = Treasury.add_new(security, market, sector, product_id, description, maturity, closing_price, discount_yield, closing_date, next_close_date, closing_mkt_price, prev_closing, next_closing, prev_closing_mkt_price, next_closing_mkt_price, EOM_mkt_price, EOY_mkt_price, EOM_date, EOY_date, prev_business_day, prev_trade_date, month_start_date, year_start_date, month_end_date, year_end_date, cost_of_funds)
    status = 200
    
    # return response
    response = Response(json.dumps(treasury), status, mimetype='application/json')
    return response

# start app
app.debug = True
app.run(port=8400)
