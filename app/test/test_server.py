import os
import sys
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models.server import Server
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app_vpn
from schemas.server_schema import ServerCreate
from crud.crud_server import create_server, delete_server, get_server

client = TestClient(app_vpn)

def test_create_server():
    server_data = {
        "name": "Test Server",
        "location": "Test Location",
        "port": 8080,
        "ip": "127.0.0.1",
        "ssh_port": 22,
        "user": "test_user",
        "password": "test_password",
        "is_running": True
    }
    
    response = client.post(
        "/servers/",
        json=server_data,
    )
    
    assert response.status_code == 200
    assert response.json()["name"] == server_data["name"]


def test_get_server_by_id():
    server_id: int = 5
    response = client.get(f"/servers/{server_id}")

    print(response.content)
    print(response.status_code)
    
    

def test_delete_server():
    server_id: int = 6
    response = client.delete(f"/servers/{server_id}")

    print(response.status_code)
    print(response.content)

    # assert response.status_code == 200
    # assert response.json() == {"detail": f"Server with id {server_id} deleted."}

def test_update_server():
    server_id: int = 8
    server_data = {
        "name": "Test Server2",
        "location": "Test Location Usa",
        "port": 8080,
        "ip": "127.0.0.1",
        "ssh_port": 22,
        "user": "test_user",
        "password": "test_password",
        "is_running": True
    }

    response = client.put(f'/servers/{server_id}', json=server_data)

    print(response.status_code)
    print(response.content)

def test_get_server_by_ip():
    ip: str = "127.0.0.1"

    response = client.get(f'/servers/ip/{ip}')

    print(response.content)
    print(response.status_code)


def test_delete_server_by_ip():
    ip: str = "127.0.0.1"

    response = client.delete(f'/servers/ip/{ip}')

    print(response.content)
    print(response.status_code)

if __name__ == "__main__":
    # test_create_server()
    # test_get_server_by_id()
    # test_delete_server()
    # test_update_server()
    # test_get_server_by_ip()
    # test_delete_server_by_ip()

    pass 
