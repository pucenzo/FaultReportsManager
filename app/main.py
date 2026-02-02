from fastapi import FastAPI
from app.routers import auth_route

app = FastAPI(title="Fault Reports Manager")

app.include_router(auth_route.router, prefix="/auth", tags=["Autenticazione"])

@app.get("/")
async def read_root():
    return {"Hello": "World"}