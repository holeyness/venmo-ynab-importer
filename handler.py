import os

from venmo_api import Client
from ynab_sdk import YNAB
from transaction import Transaction


def auth_venmo(event):
    return Client(access_token=event['venmo_access_token'])


def auth_ynab(event):
    return YNAB(event['ynab_key'])


def get_venmo_transactions(venmo_client, ynab_venmo_account_id):
    profile = venmo_client.user.get_my_profile()
    transactions = venmo_client.user.get_user_transactions(user_id=profile.id)
    return list(map(lambda x: Transaction(x, profile.username, ynab_venmo_account_id), transactions))


def record_new_transactions(venmo_transactions, existing_transactions, ynab_client, budget_id):
    imported_transaction = [transaction.serialize_ynab_transaction() for transaction in venmo_transactions]

    existing_transaction_as_set = {(transaction.date, transaction.amount, transaction.payee_name) for transaction in existing_transactions}
    missing_transactions = [transaction for transaction in imported_transaction if (transaction.date, transaction.amount, transaction.payee_name) not in existing_transaction_as_set]

    if missing_transactions:
        ynab_client.transactions.create_transactions(budget_id=budget_id, transactions=missing_transactions)


def update_uncleared_transactions(venmo_transactions, existing_transactions, ynab_client, budget_id):
    imported_transaction = [transaction.serialize_ynab_transaction() for transaction in venmo_transactions]
    imported_transaction_as_dict = {(transaction.date, transaction.amount, transaction.payee_name) for transaction in imported_transaction}

    uncleared_transactions = [transaction for transaction in existing_transactions if transaction.cleared != "cleared" and (transaction.date, transaction.amount, transaction.payee_name) in imported_transaction_as_dict]

    for transaction in uncleared_transactions:
        transaction.cleared = "cleared"
        ynab_client.transactions.update_transaction(budget_id=budget_id, transaction_id=transaction.id, transaction=transaction)


def handler(event, context):
    venmo_client = auth_venmo(event)
    ynab_client = auth_ynab(event)

    budget_id = event['budget_id']
    ynab_account_id = event['account_id']
    venmo_transactions = get_venmo_transactions(venmo_client, ynab_account_id)
    existing_transactions = ynab_client.transactions.get_transactions_from_account(budget_id=budget_id, account_id=ynab_account_id).data.transactions

    record_new_transactions(venmo_transactions, existing_transactions, ynab_client, budget_id)
    update_uncleared_transactions(venmo_transactions, existing_transactions, ynab_client, budget_id)


if __name__ == "__main__":
    payload = {
        'venmo_access_token': os.environ['VENMO_TOKEN'],
        'ynab_key': os.environ['YNAB_KEY'],
        'account_id': os.environ['YNAB_VENMO_ACCOUNT_ID'],
        'budget_id': os.environ['BUDGET_ID']
    }

    handler(payload, None)


