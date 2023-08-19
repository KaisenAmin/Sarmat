import os
import sys
from fastapi.testclient import TestClient
from main import app_vpn

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = TestClient(app_vpn)

def test_create_user():
    user_data = {
        "first_name": "John",
        "email": "john.doe@example.com",
        "password_hash": "123456"
    }
    
    response = client.post(
        "/users/",
        json=user_data,
    )
    
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    
    assert response.status_code == 200

def test_delete_user():
    user_id = 2  # Change this to the ID of the user you want to delete

    response = client.delete(f"/users/{user_id}")

    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    
    assert response.status_code == 200
    assert response.json()["detail"] == "User deleted successfully"


def test_delete_user_by_email():
    test_email = "john.doe@example.com"

    response = client.delete(f"/users/email/{test_email}")
  
    print(response.content)

    assert response.status_code == 200
    assert response.json()["detail"] == "User deleted successfully"


def test_get_list_of_users():
    response = client.get('/users/')
    
    print(response.content)

    assert response.status_code == 200 
    

def test_get_user_by_id():
    user_id: int = 3 
    response = client.get(f'/users/{user_id}')

    print(response.content)

    assert response.status_code == 200 

def test_get_user_by_email():
    email: str = 'test.user@example.com'
    response = client.get(f'/users/email/{email}')

    print(response.content)

    assert response.status_code == 200 


def test_update_user_by_id():
    user_id: int = 9
    updated_user_data = {
        "first_name": "Updated",
        "last_name": "User",
        "email": "updated.user@example.com",
        "phone": "9876543210",
        "password": "updatedpassword"
    }

    response = client.put(
        f'/users/{user_id}',
        json=updated_user_data,
    )

    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    assert response.status_code == 200
    assert response.json()["id"] == user_id
    assert response.json()["email"] == updated_user_data["email"]
    assert response.json()["first_name"] == updated_user_data["first_name"]
    assert response.json()["last_name"] == updated_user_data["last_name"]
    assert response.json()["phone"] == updated_user_data["phone"]

def test_change_password():
    response = client.post(
            "/change_password",
            json={
                "email": "testchange@example.com",
                "current_password": "123456",
                "new_password": "amin_1375",
            },
        )

    assert response.status_code == 200, response.text
    assert response.json()["detail"] == "Password successfully updated"

if __name__ == "__main__":
    test_create_user()
    #test_delete_user()
    # test_delete_user_by_email()

    # test_get_list_of_users()
    # test_get_user_by_id()
    # test_get_user_by_email()

    # test_update_user_by_id()
    # test_get_list_of_users()
    pass 