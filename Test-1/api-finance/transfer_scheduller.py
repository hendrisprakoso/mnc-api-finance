from database import (get_detail_transaction, update_account_balance_transfer, get_detail_account_by_id, update_transaction)

def transfer_amount():
    list_transfer = get_detail_transaction()
    if len(list_transfer) > 0:
        for transfer in list_transfer:
            if transfer["status"] == 'waiting':
                """ Update balance Receiver """
                target_account = get_detail_account_by_id(transfer["target_account_id"])
                if not target_account:
                    continue
                balance = target_account["balance"] + transfer["amount"]
                update_balance = update_account_balance_transfer(user_id=transfer["target_account_id"], balance=balance)
                if update_balance["status"]:
                    
                    """ Update balance Sender """
                    sender_account = get_detail_account_by_id(transfer["account_id"])
                    if not sender_account:
                        continue
                    balance = sender_account["balance"] - transfer["amount"]
                    update_balance = update_account_balance_transfer(user_id=transfer["account_id"], balance=balance)
                    if update_balance["status"]:

                        """ Update Transaction """
                        sender_account_updated = get_detail_account_by_id(transfer["account_id"])
                        upd_transaction = update_transaction(
                            balance_before = sender_account["balance"],
                            balance_after  = sender_account_updated["balance"],
                            trx_code       = transfer["trx_code"]
                        )
                        print(f"upd_transaction : {upd_transaction}")
    else:
        print(f"No have data to transfer")