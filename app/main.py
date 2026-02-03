from fastapi import FastAPI, Depends
from app.dependencies import get_current_user
from app.routers import auth_route, segnalazioni_route

app = FastAPI(title="Fault Reports Manager")

app.include_router(auth_route.router, tags=["Autenticazione"])
app.include_router(segnalazioni_route.router, tags=["Segnalazioni"])
