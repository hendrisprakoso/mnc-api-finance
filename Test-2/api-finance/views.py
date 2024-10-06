import uuid


from flask import Flask, jsonify, Response, request, send_file, abort, Response
from flask_mail import Message
from settings import app, db, config
from waitress import serve
from datetime import datetime, date, timedelta

from flask_jwt_extended import JWTManager, create_access_token

from database import (get_check_data_phone, create_new_account, get_detail_account_by_id, get_detail_account_by_phone, 
					  get_check_login, update_account_token, get_detail_account_by_token, update_account_profile, update_account_balance, add_new_transaction,
					  get_detail_transaction, get_list_transaction_by_user)
from tools import generate_uuid, masking_phone_number
from middleware import authorization_control




@app.route('/v1/register', methods=['POST'])
def account_register():

	""" Get data request and masking value request """	
	try:
		data_request = request.get_json()
		first_name 		= data_request["first_name"] 
		last_name 		= data_request["last_name"] 
		phone_number 	= masking_phone_number(data_request["phone_number"] )
		address 		= data_request["address"] 
		pin 			= data_request["pin"]
	except Exception as error:
		return jsonify({"status" : False, "message" : "Make sure your payload is in accordance with the requirements!"}), 400
	
	""" Handle validation data request """
	if not phone_number:
		return jsonify({"status" : False, "message" : "Phone number is not valid!"}), 400
	
	# Checking phone number is exist
	phone_number_is_exist = get_check_data_phone(phone_number)
	if phone_number_is_exist["count"] > 0:
		return jsonify({"status" : False, "message" : "Phone Number already registered"}), 200

	""" Add new data """
	try:
		add_new_account = create_new_account(
								user_id 		= generate_uuid(), 
								first_name 		= first_name, 
								last_name 		= last_name, 
								phone_number 	= phone_number, 
								address 		= address, 
								pin 			= pin
							)
		
		if add_new_account["status"]:
			account_detail = get_detail_account_by_phone(phone_number)
			return jsonify({"status" : True, "message" : "success", "result" : account_detail}), 200
		
		else:
			return jsonify({"status" : True, "message" : "Error Database!"}), 403 

	except Exception as error:
		return jsonify({"status" : True, "message" : f"Error Database!, detail : {str(error)}"}), 403		

@app.route('/v1/login', methods=['POST'])
def login():

	""" Get data request and masking value request """
	try:
		data_request = request.get_json()
		phone_number	 = masking_phone_number(data_request["phone_number"])
		pin				 = data_request["pin"]
	except Exception as error:
		return jsonify({"status" : False, "message" : "Make sure your payload is in accordance with the requirements!"}), 400
	
	""" Handle validation data request """
	if not phone_number:
		return jsonify({"status" : False, "message" : "Phone number is not valid!"}), 400

	check_account = get_check_login(
						phone_number	 = phone_number, 
						pin				 = pin
					)	
	if check_account["count"] == 0:
		return jsonify({"status" : False, "message" : "Phone Number and PIN doesn’t match."}), 400
	
	""" Set Token JWT """
	account_detail = get_detail_account_by_phone(phone_number)
	access_token = create_access_token(identity=account_detail["user_id"])

	try:
		update_token = update_account_token(phone_number, access_token)
	except Exception as error:
		print(error)
		return jsonify({"status" : False, "message" : "Error Database, Failed To Login."}), 403


	return jsonify({"status" : True, "message" : "success", "result" : {"access_token" : access_token}}), 200


@app.route('/v1/profile', methods=['PUT'])
@authorization_control
def update_profile():
	token = request.headers.get('Authorization', None).split(" ")[1]
	account_detail = get_detail_account_by_token(token=token)

	""" Get data request and masking value request """	
	data_request = request.get_json()
	try:
		first_name 		= data_request["first_name"]
		last_name 		= data_request["last_name"] 
		address 		= data_request["address"]
		phone_number 	= masking_phone_number(account_detail["phone_number"])
	except Exception as error:
		return jsonify({"status" : False, "message" : "Make sure your payload is in accordance with the requirements!"}), 400
	
	""" Handle validation data request """
	if not phone_number:
		return jsonify({"status" : False, "message" : "Phone number is not valid!"}), 400


	""" Add Update data """
	try:
		update_data = update_account_profile(
							first_name 		= first_name, 
							last_name 		= last_name, 
							address 		= address, 
							phone_number 	= phone_number
						)
		if not update_data["status"]:
			return jsonify({"status" : True, "message" : f"Error Database!, detail : {str(error)}"}), 403
		
		account_detail = get_detail_account_by_phone(account_detail["phone_number"])

		return jsonify({"status" : True, "message" : "success", "result" : account_detail}), 200
	except Exception as error:
		return jsonify({"status" : True, "message" : f"Error Database!, detail : {str(error)}"}), 403		


@app.route('/v1/top-up', methods=['POST'])
@authorization_control
def topup_balance():
	token = request.headers.get('Authorization', None).split(" ")[1]
	account_detail = get_detail_account_by_token(token=token)

	""" Get data request and masking value request """
	try:
		data_request = request.get_json()
		amount = data_request["amount"]
	except Exception as error:
		return jsonify({"status" : False, "message" : "Make sure your payload is in accordance with the requirements!"}), 400

	""" Handle validation data request """
	if amount < 0 or amount in ('', None):
		return jsonify({"status" : False, "message" : "Amount is not valid"}), 400

	""" Add new Transaction """
	try:
		trx_id = generate_uuid()
		# Update balance in account
		balance = account_detail["balance"] + amount
		update_balance = update_account_balance(account_detail["phone_number"], balance)
		if update_balance["status"]:
			account_detail_updated = get_detail_account_by_token(token=token)
			# Add new Transaction
			new_transaction = add_new_transaction(
									trx_code 			= trx_id, 
									amount 				= amount, 
									balance_before 		= account_detail["balance"], 
									balance_after 		= account_detail_updated["balance"], 
									account_id 			= account_detail["user_id"], 
									trx_type 			= "topup",
									status 				= "success"
								)
			if not new_transaction["status"]:
				return jsonify({"status" : False, "message" : "Error Database. Create transaction"}), 403
			

		else:
			return jsonify({"status" : False, "message" : "Error Database. Update balance"}), 403
	except Exception as error:
		return jsonify({"status" : False, "message" : "Error Database."}), 403

	transaction_detail = get_detail_transaction(trx_id)
	if transaction_detail:
		return jsonify({
			"status" : True, 
			"message" : "success",
			"result" : {
				"top_up_id" 		: transaction_detail["trx_code"],
				"amount_top_up" 	: transaction_detail["amount"],
				"balance_before" 	: transaction_detail["balance_before"],
				"balance_after" 	: transaction_detail["balance_after"],
				"created_date" 		: transaction_detail["created_at"].strftime("%Y-%m-%d %H:%M:%S"),
			}
		}), 200
	else:
		return jsonify({
			"status" : True, 
			"message" : "Failed to load detail transaction",
			"result" : None
		}), 200


@app.route('/v1/pay', methods=['POST'])
@authorization_control
def payment():
	token = request.headers.get('Authorization', None).split(" ")[1]
	account_detail = get_detail_account_by_token(token=token)

	""" Get data request and masking value request """
	try:
		data_request = request.get_json()
		amount  		= data_request["amount"]
		remarks  		= data_request["remarks"]

	except Exception as error:
		return jsonify({"status" : False, "message" : "Make sure your payload is in accordance with the requirements!"}), 400

	""" Handle validation data request """
	if amount < 0 or amount in ('', None):
		return jsonify({"status" : False, "message" : "Amount is not valid"}), 400

	""" Add new Transaction """
	try:
		trx_id = generate_uuid()
		# Update balance in account
		balance = account_detail["balance"] - amount
		update_balance = update_account_balance(account_detail["phone_number"], balance)
		if update_balance["status"]:
			account_detail_updated = get_detail_account_by_token(token=token)
			# Add new Transaction
			new_transaction = add_new_transaction(
									trx_code 			= trx_id, 
									amount 				= amount, 
									balance_before 		= account_detail["balance"], 
									balance_after 		= account_detail_updated["balance"], 
									account_id 			= account_detail["user_id"], 
									trx_type 			= "payment",
									status 				= "success",
									remarks				= remarks
								)
			if not new_transaction["status"]:
				return jsonify({"status" : False, "message" : "Error Database. Create transaction"}), 403
			

		else:
			return jsonify({"status" : False, "message" : "Error Database. Update balance"}), 403

	except Exception as error:
		return jsonify({"status" : False, "message" : "Error Database."}), 403

	transaction_detail = get_detail_transaction(trx_id)
	if transaction_detail:
		return jsonify({
			"status" : True, 
			"message" : "success",
			"result" : {
				"payment_id" 		: transaction_detail["trx_code"],
				"amount" 			: transaction_detail["amount"],
				"remarks" 			: transaction_detail["remarks"],
				"balance_before" 	: transaction_detail["balance_before"],
				"balance_after" 	: transaction_detail["balance_after"],
				"created_date" 		: transaction_detail["created_at"].strftime("%Y-%m-%d %H:%M:%S"),
			}
		}), 200
	else:
		return jsonify({
			"status" : True, 
			"message" : "Failed to load detail transaction",
			"result" : None
		}), 200




	return jsonify({"status" : True, "message" : "success"}), 200


@app.route('/v1/transfer', methods=['POST'])
@authorization_control
def transfer():

	token = request.headers.get('Authorization', None).split(" ")[1]
	account_detail = get_detail_account_by_token(token=token)

	""" Get data request and masking value request """
	try:
		data_request 	= request.get_json()
		target_account  = data_request["target_user"]
		amount  		= data_request["amount"]
		remarks  		= data_request["remarks"]
	except Exception as error:
		return jsonify({"status" : False, "message" : "Make sure your payload is in accordance with the requirements!"}), 400
	
	""" Handle validation data request """
	if amount < 0 or amount in ('', None):
			return jsonify({"status" : False, "message" : "Amount is not valid"}), 400

	if account_detail["user_id"] == target_account:
		return jsonify({"status" : False, "message" : "You can't transfer to your self!"}), 400
	
	if account_detail["balance"] < amount:
		return jsonify({"status" : False, "message" : "Balance is not enough"}), 400
	
	check_target_account = get_detail_account_by_id(target_account)
	if not check_target_account:
		return jsonify({"status" : False, "message" : "Target user is not valid!"}), 400
		

	""" Proses create transaction, with set status is waiting. data will be updated with scheduller """
	try:
		trx_id = generate_uuid()
		account_detail_updated = get_detail_account_by_token(token=token)
		# Add new Transaction
		new_transaction = add_new_transaction(
								trx_code 			= trx_id, 
								amount 				= amount, 
								balance_before 		= account_detail["balance"], 
								balance_after 		= account_detail_updated["balance"], 
								account_id 			= account_detail["user_id"], 
								trx_type 			= "transfer",
								status				= "waiting",
								remarks				= remarks,
								target_account_id	= target_account
							)
		if not new_transaction["status"]:
			return jsonify({"status" : False, "message" : "Error Database. Create transaction"}), 403

	except Exception as error:
		return jsonify({"status" : False, "message" : f"Error Database. {error}"}), 403

	""" Create response data """
	transaction_detail = get_detail_transaction(trx_id)
	if transaction_detail:
		return jsonify({
			"status" : True, 
			"message" : "success",
			"result" : {
				"transfer_id" 		: transaction_detail["trx_code"],
				"amount" 			: transaction_detail["amount"],
				"remarks" 			: transaction_detail["remarks"],
				"balance_before" 	: transaction_detail["balance_before"],
				"balance_after" 	: transaction_detail["balance_after"],
				"created_date" 		: transaction_detail["created_at"].strftime("%Y-%m-%d %H:%M:%S"),
			}
		}), 200
	else:
		return jsonify({
			"status" : True, 
			"message" : "Failed to load detail transaction",
			"result" : None
		}), 200


@app.route('/v1/transactions', methods=['GET'])
@authorization_control
def report():
	token = request.headers.get('Authorization', None).split(" ")[1]
	account_detail = get_detail_account_by_token(token=token)


	list_report = get_list_transaction_by_user(account_detail["user_id"])
	data = []
	for trx in list_report:

		temp = {
			"status" 			: trx["status"],
			"user_id" 			: trx["account_id"],
			"amount" 			: trx["amount"],
			"remarks" 			: trx["remarks"],
			"balance_before" 	: trx["balance_before"],
			"balance_after" 	: trx["balance_after"],
			"created_date" 		: trx["created_at"].strftime("%Y-%m-%d %H:%M:%S"),
		}

		if trx["trx_type"] == 'topup':
			temp["top_up_id"] 			= trx["trx_code"]
			temp["transaction_type"] 	= "CREDIT"
		
		elif trx["trx_type"] == 'payment':
			temp["payment_id"] 			= trx["trx_code"]
			temp["transaction_type"] 	= "DEBIT"

		elif trx["trx_type"] == 'transfer':
			temp["transfer_id"] 		= trx["trx_code"]
			temp["transaction_type"] 	= "DEBIT"

		else:
			temp["transaction_id"] 		= trx["trx_code"]
			temp["transaction_type"] 	= ""

		data.append(temp)

	return jsonify({"status" : True, "message" : "success", "result" : data})


if __name__ == '__main__':
	import logging
	logging.basicConfig(filename='api.log',level=logging.DEBUG)

	serve(app, host='0.0.0.0', port=5000)
