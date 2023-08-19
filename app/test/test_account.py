import os
import sys
from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app_vpn

client = TestClient(app_vpn)


def test_create_account():
    response = client.post(
        "/accounts/",
        json={"name": "Test Account", "max_users": 3, "duration_months": 1, "cost_toman": 85000, "user_ids": [1, 2]},
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Account"
    assert data["max_users"] == 2
    assert data["duration_months"] == 1
    return data["id"]


def test_get_account(account_id: int):
    response = client.get(f"/accounts/{account_id}")

    assert response.status_code == 200, response.text
    data = response.json()

    print(data)

    assert data["name"] == "Test Account"
    assert data["max_users"] == 2
    assert data["duration_months"] == 1

def test_buy_account_for_user(user_id: int):
    # Buy account for user
    response = client.post(
        f"/accounts/buy/{user_id}",
        json={
            "name": "Test Account",  # example name
            "max_users": 1,  # example max_users
            "duration_months": 1,  # example duration_months
            "cost_toman": 85000,  # example cost_toman
            "user_ids": [],  # example user_ids
        },
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    assert data["max_users"] == 1

    # Retrieve the user data to check expiration_date
    user_response = client.get(f"/users/{user_id}")
    assert user_response.status_code == 200, user_response.text
    user_data = user_response.json()
    
    # Convert the expiration_date string to datetime object
    expiration_date = datetime.strptime(user_data["expiration_date"], "%Y-%m-%dT%H:%M:%S.%f")
    
    # Check if expiration_date is set to about 30 days from now
    expected_expiration_date = datetime.now() + timedelta(days=30)
    time_difference = expected_expiration_date - expiration_date
    assert abs(time_difference.total_seconds()) < 60, "Expiration date not set correctly"

def test_buy_account_by_email(user_email: str):
    response = client.post(
        f"/accounts/buy_by_email/{user_email}",
        json={
            "name": "Test Account",
            "max_users": 2,
            "duration_months": 1,
            "cost_toman": 85000,
            "user_ids": [],
        },
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    assert data["max_users"] == 2

    # Now let's check if the expiration_date of the user has been set correctly
    user_response = client.get(f"/users/email/{user_email}")
    assert user_response.status_code == 200, user_response.text
    user_data = user_response.json()
    
    # Parse the expiration_date from the response
    expiration_date = datetime.fromisoformat(user_data["expiration_date"])
    
    # Check if the expiration_date is about one month from now
    expected_expiration = datetime.utcnow() + timedelta(days=30)
    assert (expected_expiration - expiration_date).total_seconds() < 60, "Expiration date not set correctly"



def test_account_expiration(user_email: str):
    response = client.get(f"/users/email/{user_email}")

    assert response.status_code == 200, response.text
    data = response.json()

    # Parse expiration_date from the response
    expiration_date = datetime.fromisoformat(data["expiration_date"])

    # Calculate the expected expiration_date
    expected_expiration_date = datetime.now()

    print(f"Expiration date: {expiration_date}")
    print(f"Expected expiration date: {expected_expiration_date}")
    print(f"Time difference: {(expiration_date - expected_expiration_date)}")


def test_delete_account(account_id: int):
    # Send a DELETE request to delete the account
    response = client.delete(f"/accounts/{account_id}")

    # Assert that the account was deleted successfully
    assert response.status_code == 204, response.text  # Expecting status code 204 for successful delete

    # If there is content, print it
    if response.status_code != 204:
        print(response.json())

    # Try to retrieve the account again to ensure it was deleted
    response = client.get(f"/accounts/{account_id}")

    # If there is content, print it
    if response.status_code != 404:
        print(response.json())

    # Assert that the account no longer exists
    assert response.status_code == 404, response.text


def test_update_account():
    account_id = 5  # You can set this to any valid account id that you want to test
    email_id_linked_to_account = "john.doe@example.com"  # Set this to the user id linked to the account you are updating

    # The data you want to update the account with
    update_data = {
        "max_users": 10,
        "duration_months": 2,
        "name": "Updated Account Name",
        "cost_toman": 100000,  # This will be ignored by the API, but you need to provide it anyway
    }

    # Sending PUT request to update account
    response = client.put(f"/accounts/{account_id}", json=update_data)

    # Assert that the request was successful
    assert response.status_code == 200, response.text

    # Assert that the account was updated correctly
    updated_account = response.json()
    assert updated_account['max_users'] == update_data['max_users']
    assert updated_account['duration_months'] == update_data['duration_months']
    assert updated_account['name'] == update_data['name']

    # Now check if the user's expiration_date was updated based on the new duration_months
    user_response = client.get(f"/users/email/{email_id_linked_to_account}")
    print(user_response.json())
    assert user_response.status_code == 200, user_response.text

    user = user_response.json()
    expected_expiration_date = datetime.now() + timedelta(days=30 * update_data['duration_months'])
    actual_expiration_date = datetime.fromisoformat(user['expiration_date'].replace("Z", "+00:00"))
    assert abs(actual_expiration_date - expected_expiration_date) < timedelta(seconds=5), "Expiration date not set correctly"




if __name__ == "__main__":
    # Uncomment to run testse
    # account_id = test_create_account()
    # test_get_account(2)
    # test_buy_account_by_email("john.doe@example.com")
    # test_buy_account_for_user(1)
    # test_account_expiration("john.doe@example.com")
    # test_delete_account(1)
    # test_update_account()
    pass 
