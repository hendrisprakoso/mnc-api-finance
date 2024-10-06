from settings import get_connection


def get_check_data_phone(phone_number):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        sql_query = """
                select
                    count(0) as count
                from
                    tbl_accounts 
                where 
                    phone_number = %s;
        """

        cursor.execute(sql_query, (phone_number, ))
        results = cursor.fetchone()
        return results
    except Exception as e:
        print(f"Error DATABASE : {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def get_detail_account_by_id(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        sql_query = """
                select
                    user_id,
                    first_name,
                    last_name,
                    phone_number,
                    address,
                    balance,
                    created_at as created_date
                from
                    tbl_accounts
                where 
                    user_id = %s;
        """

        cursor.execute(sql_query, (user_id, ))
        results = cursor.fetchone()
        return results
    except Exception as e:
        print(f"Error DATABASE : {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def get_detail_account_by_phone(phone_number):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        sql_query = """
                select
                    user_id,
                    first_name,
                    last_name,
                    phone_number,
                    address,
                    date_format(created_at, '%Y-%m-%d %H:%i') as created_date,
	                date_format(modified_at, '%Y-%m-%d %H:%i') as updated_date
                from
                    tbl_accounts
                where 
                    phone_number = %s;
        """

        cursor.execute(sql_query, (phone_number, ))
        results = cursor.fetchone()
        return results
    except Exception as e:
        print(f"Error DATABASE : {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def get_detail_account_by_token(token):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        sql_query = """
                select
                    user_id,
                    first_name,
                    last_name,
                    phone_number,
                    address,
                    balance,
                    created_at as created_date
                from
                    tbl_accounts
                where 
                    token = %s;
        """

        cursor.execute(sql_query, (token, ))
        results = cursor.fetchone()
        return results
    except Exception as e:
        print(f"Error DATABASE : {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def get_check_login(phone_number, pin):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        sql_query = """
                select
                    count(0) as count
                from
                    tbl_accounts 
                where 
                    phone_number = %s
                    and pin = %s;
        """

        cursor.execute(sql_query, (phone_number, pin, ))
        results = cursor.fetchone()
        return results
    except Exception as e:
        print(f"Error DATABASE : {e}")
        return None
    finally:
        cursor.close()
        connection.close()


def create_new_account(user_id, first_name, last_name, phone_number, address, pin):
    
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        sql_query = """
            INSERT INTO tbl_accounts 
                (user_id, first_name, last_name, phone_number, address, pin, token, created_at, modified_at) 
            VALUES
                (%s, %s, %s, %s, %s, %s, NULL, current_timestamp(), current_timestamp());
        """
        cursor.execute(sql_query, (
            user_id, first_name, last_name, phone_number, address, pin
        ))
        connection.commit()
        return {'status': True, 'message': 'Data Added successfully.'}
    except Exception as e:
        print(f"Error: {e}")
        return {'status': False, 'message': str(e)}
    finally:
        cursor.close()
        connection.close()


def update_account_token(phone_number, token):
    
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        sql_query = """
            update
                tbl_accounts
            set
                token = %s,
                modified_at = current_timestamp() 
            where
                phone_number = %s;
        """
        cursor.execute(sql_query, (
            token, phone_number
        ))
        connection.commit()
        return {'status': True, 'message': 'Data update successfully.'}
    except Exception as e:
        print(f"Error: {e}")
        return {'status': False, 'message': str(e)}
    finally:
        cursor.close()
        connection.close()

def update_account_profile(first_name, last_name, address, phone_number):
    
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        sql_query = """
            update
                tbl_accounts
            set
                first_name = %s,
                last_name = %s,
                address = %s,
                modified_at = current_timestamp() 
            where
                phone_number = %s;
        """
        cursor.execute(sql_query, (
            first_name, last_name, address, phone_number
        ))
        connection.commit()
        return {'status': True, 'message': 'Data update successfully.'}
    except Exception as e:
        print(f"Error: {e}")
        return {'status': False, 'message': str(e)}
    finally:
        cursor.close()
        connection.close()


def update_account_balance(phone_number, balance):
    
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        sql_query = """
            update
                tbl_accounts
            set
                balance = %s,
                modified_at = current_timestamp() 
            where
                phone_number = %s;
        """
        cursor.execute(sql_query, (
            balance, phone_number
        ))
        connection.commit()
        return {'status': True, 'message': 'Data update successfully.'}
    except Exception as e:
        print(f"Error: {e}")
        return {'status': False, 'message': str(e)}
    finally:
        cursor.close()
        connection.close()


def add_new_transaction(trx_code, amount, balance_before, balance_after, account_id, trx_type, status=None, remarks=None, target_account_id=None):
    
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        sql_query = """
            insert into tbl_transactions 
                (trx_code, amount, balance_before, balance_after, created_at, account_id, trx_type, status, remarks, target_account_id)
            values 
                (%s, %s, %s, %s, current_timestamp(), %s, %s, %s, %s, %s);
        """
        cursor.execute(sql_query, (
            trx_code, amount, balance_before, balance_after, account_id, trx_type, status, remarks, target_account_id
        ))
        connection.commit()
        return {'status': True, 'message': 'Data update successfully.'}
    except Exception as e:
        print(f"Error: {e}")
        return {'status': False, 'message': str(e)}
    finally:
        cursor.close()
        connection.close()


def get_detail_transaction(trx_code):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        sql_query = """
                select
                    trx_code,
                    amount,
                    balance_before,
                    balance_after,
                    created_at,
                    remarks
                from
                    tbl_transactions
                where
                    trx_code = %s;
        """

        cursor.execute(sql_query, (trx_code, ))
        results = cursor.fetchone()
        return results
    except Exception as e:
        print(f"Error DATABASE : {e}")
        return None
    finally:
        cursor.close()
        connection.close()


def get_detail_transaction():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        sql_query = """
                select
                    trx_code,
                    status,
                    amount,
                    account_id,
                    target_account_id,
                    remarks
                from
                    tbl_transactions
                where
                    trx_type = 'transfer'
                    and status = 'waiting';
        """
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"Error DATABASE : {e}")
        return None
    finally:
        cursor.close()
        connection.close()


def update_account_balance_transfer(user_id, balance):
    
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        sql_query = """
            update
                tbl_accounts
            set
                balance = %s,
                modified_at = current_timestamp() 
            where
                user_id = %s;
        """
        cursor.execute(sql_query, (
            balance, user_id
        ))
        connection.commit()
        return {'status': True, 'message': 'Data update successfully.'}
    except Exception as e:
        print(f"Error: {e}")
        return {'status': False, 'message': str(e)}
    finally:
        cursor.close()
        connection.close()


def update_transaction(balance_before, balance_after, trx_code):
    
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        sql_query = """
            update
                tbl_transactions
            set
                balance_before = %s,
                balance_after = %s,
                status = 'success'
            where
                trx_code = %s;
        """
        cursor.execute(sql_query, (
            balance_before, balance_after, trx_code
        ))
        connection.commit()
        return {'status': True, 'message': 'Data update successfully.'}
    except Exception as e:
        print(f"Error: {e}")
        return {'status': False, 'message': str(e)}
    finally:
        cursor.close()
        connection.close()



def get_list_transaction_by_user(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        sql_query = """
                select
                    trx_code,
                    status,
                    account_id,
                    trx_type,
                    amount,
                    remarks,
                    balance_before,
                    balance_after,
                    created_at
                from
                    tbl_transactions
                where
                    account_id = %s;
        """
        cursor.execute(sql_query, (user_id, ))
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"Error DATABASE : {e}")
        return None
    finally:
        cursor.close()
        connection.close()

