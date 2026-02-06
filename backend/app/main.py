from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.dependencies import get_current_user
from app.routers import autenticazione_route, segnalazioni_route, user_route

app = FastAPI(title="Fault Reports Manager")

"""Registriamo gli endpoint"""
app.include_router(autenticazione_route.router, tags=["Autenticazione"])
app.include_router(segnalazioni_route.router, prefix="/segnalazioni", tags=["Segnalazioni"])
app.include_router(user_route.router, tags=["Utente"])

"""definiamo le origini/siti web possono fare le richieste al backend, per ora solo il frontend Vite"""
origins = ["http://localhost:5173"]

"""
Configuriamo il CORS che controllerà ogni richiesta.
Gli passiamo gli indirizzi che possono fare richiesta.
Consente al broser di inviare token.
Accetta qualunque metodo e header HTTP.
"""
app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins, 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"], 
)