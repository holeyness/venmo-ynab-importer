import os

from venmo_api import Client
from ynab_sdk import YNAB
from transaction import Transaction

# Venmo
venmo_handle = os.environ['VENMO_HANDLE']
venmo_access_token = os.environ['VENMO_TOKEN']
venmo_client = Client(access_token=venmo_access_token)

# YNAB
ynab_key = os.environ['YNAB_KEY']
budget_id = os.environ['BUDGET_ID']
account_id = os.environ['YNAB_VENMO_ACCOUNT_ID']
ynab_client = YNAB(ynab_key)


def get_venmo_transactions():
    user_id = venmo_client.user.get_my_profile().id
    transactions = venmo_client.user.get_user_transactions(user_id=user_id)
    return list(map(lambda x: Transaction(x, venmo_handle, account_id), transactions))


def record_new_transactions(venmo_transactions, existing_transactions):
    imported_transaction = [transaction.serialize_ynab_transaction() for transaction in venmo_transactions]

    existing_transaction_as_set = {(transaction.date, transaction.amount, transaction.payee_name) for transaction in existing_transactions}
    missing_transactions = [transaction for transaction in imported_transaction if (transaction.date, transaction.amount, transaction.payee_name) not in existing_transaction_as_set]

    ynab_client.transactions.create_transactions(budget_id=budget_id, transactions=missing_transactions)


def update_uncleared_transactions(venmo_transactions, existing_transactions):
    imported_transaction = [transaction.serialize_ynab_transaction() for transaction in venmo_transactions]
    imported_transaction_as_dict = {(transaction.date, transaction.amount, transaction.payee_name) for transaction in imported_transaction}

    uncleared_transactions = [transaction for transaction in existing_transactions if transaction.cleared != "cleared" and (transaction.date, transaction.amount, transaction.payee_name) in imported_transaction_as_dict]

    for transaction in uncleared_transactions:
        transaction.cleared = "cleared"
        ynab_client.transactions.update_transaction(budget_id=budget_id, transaction_id=transaction.id, transaction=transaction)


def handler(event, context):
    venmo_transactions = get_venmo_transactions()
    existing_transactions = ynab_client.transactions.get_transactions(budget_id=budget_id).data.transactions
    record_new_transactions(venmo_transactions, existing_transactions)
    update_uncleared_transactions(venmo_transactions, existing_transactions)


if __name__ == "__main__":
    handler(None, None)


