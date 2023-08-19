from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI()

class ConnectionRequest(BaseModel):
    email: str
    password: str
    server_ip: str
    mac_address: str

# The URL of your main server
MAIN_SERVER_URL = "http://127.0.0.1:8000"

async def create_new_connection(user_id, server_id, active_connections, max_users, mac):
    async with httpx.AsyncClient() as client:
        # POST request to associate user with server
        await client.post(
            f"{MAIN_SERVER_URL}/user_server/associate/{user_id}/{server_id}",
            json={'max_connections': max_users, 'active_connections': active_connections, 'mac_address': mac}
        )

    return {"message": "A new connection has been made"}

@app.post("/request-connection")
async def request_connection(request: ConnectionRequest):
    try:
        mac_address = request.mac_address
        print(request)
        # Get user by email
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{MAIN_SERVER_URL}/users/email/{request.email}")

        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="User not found")

        db_user = response.json()
        user_id = db_user['id']
        email = db_user['email']

        # Get account
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{MAIN_SERVER_URL}/accounts/by_user/email/{email}")

        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Account not found")

        db_account = response.json()
        max_users = db_account['max_users']
        print(request.server_ip)
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{MAIN_SERVER_URL}/servers/ip/{request.server_ip}")

        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Server not found")
        
        server_id = response.json()['id']
        # Get active connections of user server
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{MAIN_SERVER_URL}/user_server/user_servers/{user_id}")
        
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="User server not found")
        print(response.text)
        response = response.json()
        active_connections = response[2]
        
        # Check conditions and create a new row in user_server table if needed
        if active_connections < max_users:
            response = await create_new_connection(user_id, server_id, active_connections + 1, max_users, mac_address)
            return {'detail': 'Connection created'}
        else:
            return {'detail': 'Max connections reached'}

        return db_user

    except KeyError:
        print("Error: The response does not contain 'active_connections'.")
        # Assuming active connections is 0
        response = await create_new_connection(user_id, server_id, 1, max_users, mac_address)
        return {'detail': 'Connection created'}

    except Exception as e:
        print("Error: ", e)
        response = await create_new_connection(user_id, server_id, 1, max_users, mac_address)
        return {'detail': 'Connection created'}


@app.post("/disconnect")
async def disconnect(request: ConnectionRequest):
    try:
        # Get user by email
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{MAIN_SERVER_URL}/users/email/{request.email}")

        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="User not found")

        db_user = response.json()
        user_id = db_user['id']
        email = db_user['email']

        # Get server by IP
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{MAIN_SERVER_URL}/servers/ip/{request.server_ip}")

        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Server not found")
        
        server_id = response.json()['id']

        # Decrease active connections
        async with httpx.AsyncClient() as client:
            await client.delete(
                f"{MAIN_SERVER_URL}/user_server/dissociate/{user_id}/{server_id}/{request.mac_address}",
            )

        return {"message": "Disconnected successfully"}

    except Exception as e:
        print("Error: ", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9123, log_level="info")
