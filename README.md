# FaultReportsManager

# Piattaforma di Segnalazioni

## Prerequisiti

Assicurarsi di avere installato sul proprio computer:

1.  **Node.js** - [Scarica qui](https://nodejs.org/)
2.  **Python 3.8+** - [Scarica qui](https://www.python.org/)

---

## Installazione e Avvio

Il progetto è diviso in due cartelle principali. Aprire due terminali diversi per eseguirli contemporaneamente.

### 1️⃣ Configurazione del Backend (Python)

Aprire il terminale nella cartella "backend":

1.  **Creare un ambiente virtuale**:
    ```
    python -m venv .venv
    ```

2.  **Attivare l'ambiente virtuale**:
    * *Windows:* ` .venv/Scripts/activate`
    * *Mac/Linux:* `source .venv/bin/activate`
    
3.  **Installare le dipendenze**:
    ```
    pip install -r requirements.txt
    ```

4.  **Inizializzare il Database**:
    ```
    python -m app.init_db
    ```

5.  **Avviare il Server**:
    ```
    uvicorn main:app --reload
    ```
    Il backend sarà attivo all'indirizzo: `http://localhost:8000`

---

### 2️⃣ Configurazione del Frontend (React)

Aprire un nuovo terminale e andare nella cartella "frontend"":

1.  **Installare i pacchetti Node**:
    ```
    npm install
    ```

2.  **Avviare il sito**:
    ```
    npm run dev
    ```
    Il frontend sarà attivo all'indirizzo: `http://localhost:5173`

---

## 🧪 Come testare l'App

1.  Andrea alla pagina di registrazione all'indirizzo (`http://localhost:5173/registrazione`).
2.  Creare un nuovo utente cliente.
3.  Fare il login.
4.  Creare una nuova segnalazione dalla dashboard.

**Per testare l'utente operatore, accreditare manualmente l'utente (consiglio tramite DB Browser for SQLite)**. Dopodichè, fare il login all'indirizzo (`http://localhost:5173/registrazione`). 

**IMPORTANTE! Per generare una password hashate è necessario eseguire da terminale il seguente comando**:
```
python -c "from passlib.context import CryptContext; ctx = CryptContext(schemes=['bcrypt'], deprecated='auto'); print(ctx.hash('admin123'))"    
```

---

## 📚 Swagger UI - fastAPI

FastAPI genera automaticamente la documentazione, visualizzabile all'indirizzo `http://localhost:8000/docs`. 

Qui è possibile vedere e testare tutte le rotte direttamente dal browser.