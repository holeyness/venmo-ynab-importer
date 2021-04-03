import time

from ynab_sdk.api.models.requests.transaction import TransactionRequest


def convert_epoch_to_date(epoch):
    return time.strftime('%Y-%m-%d', time.localtime(epoch))


def convert_to_miliunits(amount):
    return int("{:.0f}".format(amount * 1000))


class Transaction:
    def __init__(self, transaction, venmo_user_handle, ynab_venmo_account_id):
        self.id = id
        self.transaction = transaction
        self.venmo_user_handle = venmo_user_handle
        self.ynab_venmo_account_id = ynab_venmo_account_id

    def __repr__(self):
        transaction = self.transaction
        return f"{transaction.payment_id} on {convert_epoch_to_date(transaction.date_completed)}: {transaction.actor.display_name} {transaction.payment_type} {transaction.target.display_name} for ${transaction.amount} / {transaction.note}"

    # Charge / Pay
    # Actor / target
    def get_transaction_amount(self):
        if self.transaction.actor.username == self.venmo_user_handle:
            # If I am the actor
            if self.transaction.payment_type == "charge":
                # If I charge someone
                return convert_to_miliunits(self.transaction.amount)
            else:
                # If I pay someone
                return convert_to_miliunits(-1 * self.transaction.amount)
        else:
            # if someone else is the actor
            if self.transaction.payment_type == "charge":
                # If someone else charges me
                return convert_to_miliunits(-1 * self.transaction.amount)
            else:
                # if someone pays me
                return convert_to_miliunits(self.transaction.amount)

    def get_payee(self):
        if self.transaction.actor.username == self.venmo_user_handle:
            return self.transaction.target.display_name
        else:
            return self.transaction.actor.display_name

    def serialize_ynab_transaction(self):
        return TransactionRequest(date=convert_epoch_to_date(self.transaction.date_completed),
                                  amount=self.get_transaction_amount(),
                                  account_id=self.ynab_venmo_account_id,
                                  payee_name=self.get_payee(),
                                  cleared="cleared",
                                  memo=self.transaction.note)
