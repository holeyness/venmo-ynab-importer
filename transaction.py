import datetime
import pytz
from ynab_sdk.api.models.requests.transaction import TransactionRequest

tz = pytz.timezone('America/New_York')


def convert_epoch_to_date(epoch):
    dt = datetime.datetime.fromtimestamp(epoch, tz)
    return dt.strftime('%Y-%m-%d')


def convert_to_miliunits(amount):
    return int("{:.0f}".format(amount * 1000))


class Transaction:
    def __init__(self, transaction, venmo_user_handle, ynab_venmo_account_id):
        self.id = id
        self.transaction = transaction
        self.venmo_user_handle = venmo_user_handle
        self.ynab_venmo_account_id = ynab_venmo_account_id
        self.category_id = None

    def __repr__(self):
        transaction = self.transaction
        return f"{transaction.payment_id} on {self.get_date()}: {transaction.actor.display_name} {transaction.payment_type} {transaction.target.display_name} for ${transaction.amount} / {transaction.note}"

    def get_date(self):
        return convert_epoch_to_date(self.transaction.date_completed or self.transaction.date_created or self.transaction.date_updated)

    def add_category_id(self, category_id):
        self.category_id = category_id

    def get_note(self):
        return self.transaction.note

    @property
    def _user_is_actor(self) -> bool:
        return self.transaction.actor.username.lower() == self.venmo_user_handle.lower()

    # Charge / Pay
    # Actor / target
    def get_transaction_amount(self):
        if self._user_is_actor:
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
        if self._user_is_actor:
            return self.transaction.target.display_name
        else:
            return self.transaction.actor.display_name

    def serialize_ynab_transaction(self):
        return TransactionRequest(date=self.get_date(),
                                  amount=self.get_transaction_amount(),
                                  account_id=self.ynab_venmo_account_id,
                                  payee_name=self.get_payee(),
                                  category_id=self.category_id,
                                  cleared="cleared",
                                  memo=self.transaction.note)
