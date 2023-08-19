import requests
import os
import sys
from main import app
from fastapi.testclient import TestClient
import uuid 


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = TestClient(app)

def get_mac_addr():
    mac_address = uuid.getnode()
    mac_address_hex = ':'.join(['{:02x}'.format((mac_address >> elements) & 0xff) for elements in range(0,8*6,8)][::-1])

    return mac_address_hex

def test_request_connection():

    try:
        data = {
            "email": "john.doe@example.com",
            "password": "123456",
            "server_ip": "157.245.46.239",
            "mac_address": get_mac_addr()
        }
        
        user_response = client.post(
            "/request-connection/",
            json=data,
        )

        print(user_response.json())

    except KeyError:
        print("Error: The response does not contain 'active_connections'.")
        active_connections = 0

    except Exception as e:
        print("An unexpected error occurred:", e)
        active_connections = 0
    # Send a POST request to the endpoint

def test_disconnect():

    try:
        # Data for the disconnect request
        data = {
            "email": "john.doe@example.com",
            "password": "123456",
            "server_ip": "157.245.46.239",
            "mac_address": get_mac_addr()
        }

        # Send a POST request to the disconnect endpoint
        user_response = client.post(
            "/disconnect",
            json=data,
        )

        # Output the response JSON
        print(user_response.json())

    except Exception as e:
        print("An unexpected error occurred:", e)


if __name__ == "__main__":
    # test_request_connection()
    test_disconnect()
