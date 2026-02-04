from fastapi import FastAPI, Depends
from app.dependencies import get_current_user
from app.routers import autenticazione_route, segnalazioni_route

app = FastAPI(title="Fault Reports Manager")

app.include_router(autenticazione_route.router, tags=["Autenticazione"])
app.include_router(segnalazioni_route.router, tags=["Segnalazioni"])
