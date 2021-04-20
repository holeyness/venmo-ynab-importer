from venmo_api import Client


def authorize():
    venmo_email = input("Venmo email: ")
    venmo_password = input("Venmo password: ")
    access_token = Client.get_access_token(username=venmo_email, password=venmo_password)
    print(access_token)


if __name__ == "__main__":
    authorize()
