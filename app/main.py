from fastapi import FastAPI
from services import user_service, server_service, log_service, auth_router, account_service, user_server_service
import uvicorn 


app_vpn = FastAPI()

app_vpn.include_router(user_service.router, prefix="/users", tags=["users"])
app_vpn.include_router(server_service.router, prefix="/servers", tags=["servers"])
app_vpn.include_router(log_service.router, prefix="/logs", tags=["logs"])
app_vpn.include_router(auth_router.router, tags=["auth"])
app_vpn.include_router(account_service.router, prefix="/accounts", tags=["accounts"])
app_vpn.include_router(user_server_service.router, prefix="/user_server", tags=["user_server"])

if __name__ == '__main__':
    print("in application")
    uvicorn.run("main:app_vpn", host="0.0.0.0", port=8000, log_level="info", reload=True)   