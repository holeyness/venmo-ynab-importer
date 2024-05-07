from venmo_api import Client


def authorize():
    venmo_email = input("Venmo email: ")
    venmo_password = input("Venmo password: ")
    # Log in on a device and pull device_id from network tab (aka "v_id" cookie)
    trusted_device_id = input("Device id: ")
    access_token = Client.get_access_token(username=venmo_email, password=venmo_password, device_id=trusted_device_id)
    print(access_token)


if __name__ == "__main__":
    authorize()
